# Online Entrance Preparation System

<br>

Online Entrance Preparation System is a 4th Semester / 2nd year University Project of Bachelor in Computer Application (BCA) designed to assist students in effective preparation for various entrance examinations. The project aims to furnish a comprehensive and user-friendly platform to augment their knowledge, refine their skills, and enhance their performance in entrance exams.

The online entrance preparation system includes practice questions, mock tests, and interactive quizzes aligned with popular exam syllabuses. It adopts a personalized learning approach, enabling students to identify strengths and weaknesses for targeted improvements. The platform also facilitates online access for self-paced study, fostering an engaging learning environment to maximize potential and boost confidence for entrance exams."

## Getting Started

If you are new to the project, here are some initial steps to get started:

**1. Clone the project**

```
git clone https://github.com/ghanteyyy/Online-Entrance-Preparation.git
```

**2. Install Dependencies**

```
pip install -r requirements.txt
```

**3. Configure Database**

```
python manage.py makemigrations
```

```
python manage.py migrate
```

**4. Run the server**

```
python manage.py runserver
```

**5. Open following URL in your web browser**

```
127.0.0.1:8000/
```

## Optional Database Configurations

The following configurations are necessary solely for the purpose of generating dummy data for testing.
<br><br>
**1. Populate Questions**

```
python mange.py PopulateQuestions
```

> If you encounter any errors, please ensure that the "Questions.json" file exists within the "static" directory and its contents are formatted correctly as JSON.

**2. Populate Users**

```
python manage.py PopulateUsers
```

**3. Populate Results for respective user**

```
python manage.py PopulateResults
```

## Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Django
- **Database:** postgresql
