import datetime
import requests
from .models import *


def compare_date(from_db, from_user, format='%Y-%m-%d'):
    """
    Compare two date strings using the specified format
    """

    if from_db is None:
        return False

    try:
        from_db = datetime.datetime.strptime(from_db, format).date()

    except ValueError:
        from_db = datetime.datetime.strptime(from_db, "%Y-%m-%dT%H:%M:%S.%fZ").date()

    from_user = datetime.datetime.strptime(from_user, format).date()

    return from_db == from_user


class UserFilter:
    """
    Utility class for filtering users based on various criteria
    """

    def __init__(self, host_url, searching_value):
        self.searching_value = searching_value
        self.data = requests.get(f'http://{host_url}/api/users').json()

    def SearchByEmail(self, search_type):
        """
        Filter users by email

        Returns:
            List: A list of users matching the specified email
        """

        return list(filter(lambda value: value[search_type] == self.searching_value, self.data))

    def SearchByDOB(self, search_type):
        """
        Filter users by date of birth

        Returns:
            List: A list of users matching the specified date of birth
        """

        return list(filter(lambda value: compare_date(value[search_type], self.searching_value), self.data))

    def SearchByGender(self, search_type):
        """
        Filter users by gender

        Returns:
            List: A list of users matching the specified gender
        """

        gender = self.searching_value.lower()[0]

        return list(filter(lambda value: value[search_type] and value[search_type][0] == gender, self.data))

    def SearchByMemberSince(self, search_type):
        """
        Filter users by the date they became members

        Returns:
            List: A list of users who became members on the specified date
        """

        return list(filter(lambda value: compare_date(value[search_type], self.searching_value), self.data))

    def SearchByAdmin(self, is_admin=True):
        """
        Filter users by admin status

        Parameters:
            is_admin (bool): If True, filter for admin users; if False, filter for non-admin users

        Returns:
            List: A list of users matching the specified admin status
        """

        return list(filter(lambda value: value['is_superuser'] == is_admin, self.data))

    def SearchByActive(self, is_active=True):
        """
        Filter users by active status

        Parameters:
            is_active (bool): If True, filter for active users; if False, filter for inactive users

        Returns:
            List: A list of users matching the specified active status
        """

        return list(filter(lambda value: value['is_active'] == is_active, self.data))


class UsersExamsFilter:
    """
    Utility class for filtering exams based on various criteria
    """

    def __init__(self, host_url, searching_value):
        self.searching_value = searching_value
        self.data = requests.get(f'http://{host_url}/api/users_exams').json()

    def SearchByEmail(self, search_type):
        """
        Filter exams by user's email

        Returns:
            List: A list of exams taken by the specified user's email
        """

        return list(filter(lambda value: value[search_type].lower() == self.searching_value.lower(), self.data))

    def SearchByUsername(self, search_type):
        """
        Filter exams by user's username

        Returns:
            List: A list of exams taken by the specified user's username
        """

        def check_username(from_db):
            """
            Check if there is any common word between the provided 'from_db'
            string and the searching value in the current instance
            """

            from_db = set(from_db.lower().split())
            from_user = set(self.searching_value.lower().split())

            return (from_db & from_user) != set()

        return list(filter(lambda value: check_username(value[search_type].lower()), self.data))

    def SearchByTestsTaken(self, search_type):
        """
        Filter exams by the total number of tests taken

        Returns:
            List: A list of exams with the specified total number of tests taken
        """

        if self.searching_value.isdigit() is False:
            return []

        self.searching_value = int(self.searching_value)

        return list(filter(lambda value: value[search_type] == self.searching_value, self.data))

    def SearchByDate(self):
        """
        Filter exams by date

        Returns:
            List: A list of exams taken on the specified date
        """

        programmes = []
        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        for detail in Exams.objects.all():
            if detail.Date == date:
                programmes.append(detail)

        return programmes


class UsersExamsProgrammeListsFilter:
    """
    Utility class for filtering exams based on various criteria
    """

    def __init__(self, host, user_id, searching_value):
        self.searching_value = searching_value
        self.data = requests.get(f'http://{host}/api/users_exams_each_programmes/{user_id}').json()

    def SearchByProgrammeName(self):
        """
        Filter exams by programme name

        Returns:
            List: A list of exams matching the specified programme name
        """

        if self.data:
            searching_value = self.searching_value.upper()

            for d in self.data:
                value = d['programme_data'][searching_value]

                d['programme_data'] = {searching_value: value}

        return self.data

    def SearchByTestsTaken(self):
        """
        Filter exams by the total number of tests taken

        Returns:
            List: A list of exams with the specified total number of tests taken
        """

        if self.searching_value.isdigit() is False or not self.data:
            return []

        searching_value = int(self.searching_value)

        for d in self.data:
            new_program_data = dict()

            for programme, value in d['programme_data'].items():
                if value == searching_value:
                    new_program_data.update({programme: value})

            if new_program_data:
                d['programme_data'] = new_program_data

        return self.data

class DetailedExamsFilter:
    """
    Utility class for filtering exams based on various criteria
    """

    def __init__(self, host, user_id, programme, searching_value):
        self.searching_value = searching_value.lower()
        self.data = requests.get(f'http://{host}/api/exams/{user_id}/{programme}').json()

    def SearchByDate(self, search_type):
        """
        Filter exams by date

        Returns:
            List: A list of exams taken on the specified date
        """

        return list(filter(lambda value: compare_date(value[search_type], self.searching_value), self.data))

    def SearchByTotalCorrectAnswered(self, search_type):
        """
        Filter exams by total correct answered by user

        Returns:
            List: A list of exams taken on the specified total correct answered by user
        """

        if self.searching_value.isdigit() is False:
            return []

        self.searching_value = int(self.searching_value)
        return list(filter(lambda value: value[search_type] == self.searching_value, self.data))


class SubjectFilter:
    """
    Utility class for filtering subjects based on various criteria
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByProgrammeName(self, host, api_url):
        """
        Filter subjects by program name

        Returns:
            List: A list of subjects matching the specified program name
        """

        programmes = requests.get(f'http://{host}/api/{api_url}').json()
        programmes = filter(lambda programme: programme['Name'].lower() == self.searching_value.lower(), programmes)

        return list(programmes)

    def SearchByTotalSubjects(self, host, api_url):
        """
        Filter subjects by total number of subjects

        Returns:
            List: A list of subjects matching the total number of subjects
        """

        searching_value = int(self.searching_value)
        programmes = requests.get(f'http://{host}/api/{api_url}').json()
        programmes = filter(lambda programme: programme['TotalQuestions'] == searching_value, programmes)

        return list(programmes)

    def SearchBySubjectName(self, host, programme):
        """
        Filter subjects by subject name

        Returns:
            List: A list of subjects matching the specified subject name
        """

        subjects = requests.get(f'http://{host}/api/subjects/{programme}').json()
        subjects = list(filter(lambda subject: subject['Name'].lower() == self.searching_value.lower(), subjects))

        return subjects

    def SearchByTotalQuestionsToSelect(self, host, programme, api_url):
        """
        Filter subjects by the total number of questions to select

        Returns:
            List: A list of subjects matching the specified total number of questions to select
        """

        programmes = requests.get(f'http://{host}/api/{api_url}/{programme}').json()
        programmes = filter(lambda programme: programme['TotalQuestionsToSelect'] == int(self.searching_value), programmes)

        return list(programmes)


class QuestionProgrammeFilter:
    """
    Utility class for filtering questions based on various criteria
    """

    def __init__(self, host, searching_value):
        self.searching_value = searching_value
        self.data = requests.get(f'http://{host}/api/questions').json()

    def SearchByProgramme(self):
        """
        Filter programme by programme name

        Returns:
            List: A list of programme matching the specified programme name
        """

        return [data for data in self.data if data['Name'].lower() == self.searching_value.lower()]

    def SearchByTotalQuestions(self):
        """
        Filter programme by total question

        Returns:
            List: A list of programme matching the specified total question
        """

        searching_value = int(self.searching_value)

        return [data for data in self.data if data['TotalQuestions'] == searching_value]


class QuestionPerProgrammeFilter:
    """
    Utility class for filtering questions based on various criteria
    """

    def __init__(self, host, programme, searching_value):
        self.searching_value = searching_value
        self.data = requests.get(f'http://{host}/api/questions/{programme}').json()

    def SearchBySubject(self):
        """
        Filter subjects by subject name

        Returns:
            List: A list of subjects matching the specified subject name
        """

        return [data for data in self.data if data['Name'].lower() == self.searching_value.lower()]

    def SearchByTotalQuestions(self):
        """
        Filter programme by total question

        Returns:
            List: A list of programme matching the specified total question
        """

        searching_value = int(self.searching_value)

        return [data for data in self.data if data['TotalQuestions'] == searching_value]


class QuestionFilter:
    """
    Utility class for filtering questions based on various criteria
    """

    def __init__(self, host, programme, subject, searching_value):
        self.searching_value = searching_value
        self.data = requests.get(f'http://{host}/api/questions/{programme}/{subject}').json()

    def SearchByTitle(self):
        """
        Filter questions by title

        Returns:
            List: A list of questions matching the specified title
        """

        return list(filter(lambda question: question['Title'].lower() == self.searching_value.lower(), self.data))

    def SearchByAnswer(self):
        """
        Filter questions by answer

        Returns:
            List: A list of questions matching the specified answer
        """

        return list(filter(lambda question: question['Answer'].lower() == self.searching_value.lower(), self.data))

    def SearchByOptions(self):
        """
        Filter questions by options

        Returns:
            List: A list of questions matching the specified options
        """

        return list(filter(lambda question: self.searching_value.lower() in question['Options'].lower(), self.data))


class ReportFilter:
    """
    Utility class for filtering reports based on various criteria
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByUser(self):
        """
        Filter reports by user

        Returns:
            List: A list of reports related to the specified user
        """

        user = CustomUser.objects.filter(email=self.searching_value).first()
        user = ReportQuestion.objects.filter(UserID=user).first()

        if user:
            return user

        return []

    def SearchByQuestion(self):
        """
        Filter reports by question

        Returns:
            List: A list of reports related to the specified question
        """

        issues = []

        for issue in ReportQuestion.objects.all():
            if issue.QuestionID.Title.lower().strip() == self.searching_value.lower().strip():
                issues.append(issue)

        return issues

    def SearchByIssue(self):
        """
        Filter reports by issue

        Returns:
            List: A list of reports related to the specified issue
        """

        issues = []

        for issue in ReportQuestion.objects.all():
            if self.searching_value.lower() == issue.Issue.lower():
                issues.append(issue)

        return issues

    def SearchByDate(self):
        """
        Filter reports by date

        Returns:
            List: A list of reports related to the specified date
        """

        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        return ReportQuestion.objects.filter(Date=date)

    def SearchByMarked(self, is_marked=True):
        """
        Filter reports by marked status

        Parameters:
            is_marked (bool): If True, filter for marked reports; if False, filter for unmarked reports

        Returns:
            List: A list of reports matching the specified marked status
        """

        return ReportQuestion.objects.filter(IsMarked=is_marked)


class FeedbackFilter:
    """
    Utility class for filtering feedback based on various criteria
    """

    def __init__(self, searching_value):
        self.searching_value = searching_value

    def SearchByName(self):
        """
        Filter feedback by name

        Returns:
            List: A list of feedback matching the specified name
        """

        feedbacks = []

        for feedback in FeedBack.objects.all():
            if self.searching_value.lower() == feedback.Name.lower():
                feedbacks.append(feedback)

        return feedbacks

    def SearchByEmail(self):
        """
        Filter feedback by email

        Returns:
            List: A list of feedback matching the specified email
        """

        return FeedBack.objects.filter(Email=self.searching_value)

    def SearchByMessage(self):
        """
        Filter feedback by message content

        Returns:
            List: A list of feedback matching the specified message content
        """

        feedbacks = []

        for feedback in FeedBack.objects.all():
            if self.searching_value.lower() == feedback.Message.lower():
                feedbacks.append(feedback)

        return feedbacks

    def SearchByMarked(self, is_marked=True):
        """
        Filter feedback by marked status

        Parameters:
            is_marked (bool): If True, filter for marked feedback; if False, filter for unmarked feedback

        Returns:
            List: A list of feedback matching the specified marked status
        """

        return FeedBack.objects.filter(IsMarked=is_marked)

    def SearchByDate(self):
        """
        Filter feedback by date

        Returns:
            List: A list of feedback matching the specified date
        """

        date = datetime.datetime.strptime(self.searching_value, '%Y-%m-%d').date()

        return FeedBack.objects.filter(Date=date)
