from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import ast


class PlagiarismChecker:

    def __init__(self):
        self.tokenizer, self.model = self.__initialize_model_and_tokenizer()

    @staticmethod
    def __initialize_model_and_tokenizer():
        tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        model = AutoModel.from_pretrained("microsoft/codebert-base", output_hidden_states=True)
        return tokenizer, model

    def __tokenize_code(self, code, max_length=512):
        return self.tokenizer(code, return_tensors='pt', padding=True, truncation=True, max_length=max_length)

    def __get_hidden_states(self, outputs, num_layers=4):
        hidden_states = outputs.hidden_states[-num_layers:]  # Last `num_layers` layers
        hidden_states = torch.stack(hidden_states, dim=0)  # Shape: (num_layers, batch_size, seq_len, hidden_size)

        hidden_states = torch.mean(hidden_states, dim=0)
        hidden_states = torch.mean(hidden_states, dim=1)

        return hidden_states

    @staticmethod
    def __normalize_vector(vector):
        return torch.nn.functional.normalize(vector, p=2, dim=1)

    @staticmethod
    def __compute_cosine_similarity(vec1, vec2):
        return torch.nn.functional.cosine_similarity(vec1, vec2).item()

    @staticmethod
    def __extract_code_features(code):
        tree = ast.parse(code)
        features = {
            "num_functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "num_for_loops": len([n for n in ast.walk(tree) if isinstance(n, ast.For)]),
            "num_while_loops": len([n for n in ast.walk(tree) if isinstance(n, ast.While)]),
            "num_if_statements": len([n for n in ast.walk(tree) if isinstance(n, ast.If)]),
            "num_return_statements": len([n for n in ast.walk(tree) if isinstance(n, ast.Return)]),
            "num_assignments": len([n for n in ast.walk(tree) if isinstance(n, ast.Assign)]),
            "num_imports": len([n for n in ast.walk(tree) if isinstance(n, ast.Import)] + [n for n in ast.walk(tree) if
                                                                                           isinstance(n,
                                                                                                      ast.ImportFrom)])
        }
        return np.array(list(features.values()))

    @staticmethod
    def __compute_tfidf_similarity(code1, code2):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([code1, code2])
        cosine_sim = (tfidf_matrix * tfidf_matrix.T).toarray()
        return cosine_sim[0, 1]

    @staticmethod
    def calculate_plagiarism(code1, code2):
        checker = PlagiarismChecker()

        # Tokenize code
        inputs1 = checker.__tokenize_code(code1)
        inputs2 = checker.__tokenize_code(code2)

        # Get hidden states representing the code
        with torch.no_grad():
            outputs1 = checker.model(**inputs1)
            outputs2 = checker.model(**inputs2)

        # Extract hidden states from the last few layers and aggregate
        hidden_states1 = checker.__get_hidden_states(outputs1)
        hidden_states2 = checker.__get_hidden_states(outputs2)

        # Normalize vectors
        hidden_states1 = checker.__normalize_vector(hidden_states1)
        hidden_states2 = checker.__normalize_vector(hidden_states2)

        # Compute cosine similarity between feature vectors
        bert_similarity = checker.__compute_cosine_similarity(hidden_states1, hidden_states2)

        # Extract traditional code features
        # This method uses compile() method, so should use try catch
        try:
            features1 = checker.__extract_code_features(code1)
        except Exception as e:
            features1 = 0.5
        try:
            features2 = checker.__extract_code_features(code2)
        except Exception as e:
            features2 = 0.5

        # Normalize features
        features1 = features1 / np.linalg.norm(features1)
        features2 = features2 / np.linalg.norm(features2)

        # Compute cosine similarity between traditional code features
        ast_similarity = np.dot(features1, features2)

        # Compute TF-IDF similarity between code snippets
        tfidf_similarity = checker.__compute_tfidf_similarity(code1, code2)

        # Combine results from CodeBERT, traditional features, and TF-IDF
        combined_similarity = (bert_similarity + ast_similarity + tfidf_similarity) / 3

        return {
            "bert_similarity": bert_similarity,
            "ast_similarity": ast_similarity,
            "tfidf_similarity": tfidf_similarity,
            "combined_similarity": combined_similarity
        }
