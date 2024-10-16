# Python Tasks Web Application

This web application allows users to create and manage groups, assign tasks to members, and evaluate code submissions. It includes an automatic plagiarism detection system and supports two submission methods: writing tasks directly on the site or uploading them as files. The app is built using **Django**, **Tailwind CSS**, and **Docker**.

## Application Features

### Group and Task Management

- **Group Creation**: Any user can create their own group and invite other users to join.
- **Task Creation**: Users can create tasks within their groups and assign them to members.
- **Task Submission**: Members can submit tasks either by typing the code directly in the online editor or by uploading a file. The system will automatically run the tests on the submitted code.

### Plagiarism Detection

The app includes a system for automatic plagiarism detection. It calculates a similarity score for each submission using three different methods:
1. **Natural Language Processing (NLP)**: Uses **Transformers** library to compare submissions.
2. **Feature Extraction**: Uses **Scikit-learn** to calculate similarity scores based on extracted features.
3. **Keyword Analysis**: A traditional method that counts occurrences of programming keywords (e.g., `def`, `if`, etc.).

If the similarity score is:
- **>= 99**: The submission is highlighted in red.
- **>= 95**: The submission is highlighted in yellow.

### Code Execution and Testing

- When users submit tasks, the system will execute the submitted function automatically based on the task’s function name.
- The system checks if the function name exists in the submission. If it’s missing, the test will result in an error.
- The execution time of the submission is also measured and reported.

### User Registration

- Users can register by providing their full name, username, and password.
- Email confirmation is required to activate the account, using **Mailtrap** as a test environment.

## Technologies Used

- **Django**: Backend framework for handling business logic and database interactions.
- **Tailwind CSS**: For building a responsive and modern user interface.
- **Docker**: Containerizes the application to ensure consistent deployment.
- **Transformers (Hugging Face)**: For advanced NLP-based plagiarism detection.
- **Scikit-learn**: Used for calculating similarity metrics between code submissions.
- **Mailtrap**: Used for sending test emails during the registration process.

## Prerequisites

Make sure you have the following installed:
- **Docker** and **Docker Compose**
- **Python 3.x**

## Installation

### 1. Clone the repository:
```bash
git clone <repository-url>
cd python-tasks-web-app-master
```

### 2. Set up Docker:

The project is Dockerized, so you can set it up with the following commands:
```bash
docker-compose build
docker-compose up
```

### 3. Access the Application:

Once the containers are up, you can access the application at `http://localhost:8000`.

### 4. Set up Environment Variables:

Configure Mailtrap credentials and any other necessary environment variables in the Docker environment file.

### 5. Run Database Migrations:

Before using the app, you need to apply migrations to set up the database:
```bash
docker-compose run web python manage.py migrate
```

## Running the Application

### Starting the App

After running `docker-compose up`, the application will be accessible at `http://localhost:8000`.

### Admin Panel

You can access the Django admin panel at `http://localhost:8000/admin`. Make sure to create a superuser by running:
```bash
docker-compose run web python manage.py createsuperuser
```
