import datetime
from Users.models import *
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model

    This serializer is used to convert the CustomUser model instances into a
    Python data type that can be easily rendered into JSON. It specifies the
    fields to include when serializing the CustomUser model

    Attributes:
        model (Model): The CustomUser model which this serializer is based on
        fields (list): The fields to be included in the serialization process,
                       including 'id', 'FullName', 'email', 'DOB', 'ProfileImage',
                       'MemberSince', 'Gender', 'is_superuser', and 'is_active'
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'FullName', 'email', 'DOB', 'ProfileImage', 'MemberSince', 'Gender', 'is_superuser', 'is_active']


class UsersExamsSerializers(serializers.ModelSerializer):
    """
    Serializes the CustomUser model for representing user information related to exams

    Attributes:s
        email (str): The email address of the user
        FullName (str): The full name of the user
        TestsTaken (int): The number of tests taken by the user
        ProfileImage (str): The URL or path to the user's profile image
    """

    TestsTaken = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'FullName', 'TestsTaken', 'ProfileImage']

    def get_TestsTaken(self, obj):
        """
        Get the total number of tests taken by a user

        Parameters:
            obj (CustomUser): The CustomUser instance for which total number of tests taken by a user is to be retrieved

        Returns:
            str: The total number of tests taken by a user
        """

        return Exams.objects.filter(UserID=obj).count()


class UsersExamsInEachProgrammeSerializers(serializers.ModelSerializer):
    """
    Serializer for the UsersExamsInEachProgramme model

    This serializer is designed to represent the ResultsExtraDetails model,
    providing a customized representation for specific fields

    Fields:
        UserID: Represents the user ID associated with the exam results
        BCA: Represents the result details for the BCA program
        BIT: Represents the result details for the BIT program
        BIM: Represents the result details for the BIM program
        BSCSIT: Represents the result details for the BSCSIT program

    Methods:
        get_UserID(obj): Custom method to retrieve the user ID from the given object

    """

    UserID = serializers.SerializerMethodField()
    UserEmail = serializers.SerializerMethodField()
    programme_data = serializers.SerializerMethodField()

    class Meta:
        model = ResultsExtraDetails
        fields = ['UserID', 'UserEmail', 'programme_data']

    def get_UserID(self, obj):
        """
        Custom method to retrieve the user ID from the given object

        Parameters:
            obj: An instance of ResultDetails representing exam results

        Returns:
            The user ID associated with the exam results
        """

        return obj.UserID.id

    def get_UserEmail(self, obj):
        """
        Custom method to retrieve the user email from the given object

        Parameters:
            obj: An instance of ResultDetails representing exam results

        Returns:
            The user email associated with the exam results
        """

        return obj.UserID.email

    def get_programme_data(self, obj):
        '''
        Custom method to retrieve the number of tests taken in respective programme
        '''

        data = dict()

        for programme in Programme.objects.all():
            prog = programme.Name.upper()
            total_tests = ResultDetails.objects.filter(ResultID__UserID=obj.UserID, ResultID__ProgrammeName__iexact=prog).count()

            data[prog] = total_tests // 100

        return data


class ExamSerializers(serializers.ModelSerializer):
    """
    Serializer for the Exams model, extending the ModelSerializer class

    Attributes:
        user_email (serializers.SerializerMethodField): A SerializerMethodField to retrieve the user's email

    Methods:
        get_user_email(obj): A method to retrieve the email of the user associated with the exam
    """

    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Exams
        fields = ['ID', 'Slug', 'user_email', 'ProgrammeName', 'CorrectCounter', 'Date', 'UserID']

    def get_user_email(self, obj):
        """
        Get the email of the user associated with the exam

        Parameters:
            obj (Exams): The Exam instance for which the user's email is to be retrieved

        Returns:
            str: The email of the user associated with the exam
        """

        return obj.UserID.email


class ProgrammeSerializers(serializers.ModelSerializer):
    """
    Serializes Programme model data for use in API responses

    This serializer class is built upon the ModelSerializer provided by the Django REST framework
    It automatically generates serialization and deserialization logic based on the Programme model

    Attributes:
        - model: The Django model (Programme) associated with this serializer
        - fields: Specifies the fields to be included in the serialization. '__all__' includes all fields
    """

    class Meta:
        model = Programme
        fields = '__all__'


class SubjectProgrammesSerializers(serializers.ModelSerializer):
    """
    Serializer for the 'Programme' model

    This serializer extends the 'ModelSerializer' provided by the
    Django REST framework and includes a custom field 'TotalQuestions'
    using 'SerializerMethodField'

    Attributes:
        TotalSubjects: A custom serializer method field that counts the number
                       of subjects within given programme
    """

    TotalQuestions = serializers.SerializerMethodField()

    class Meta:
        model = Programme
        fields = ['Name', 'TotalQuestions']

    def get_TotalQuestions(self, obj):
        """
        Custom serializer method to retrieve the total number of
        questions of 'Programme' object associated with the 'Subject'

        Parameters:
            obj: The 'Programme' instance being serialized

        Returns:
            str: Total number of the associated 'Subject' object
        """

        return Subject.objects.filter(ProgrammeID__Name__iexact=obj.Name).count()


class SubjectProgrammeSerializers(serializers.ModelSerializer):
    """
    Serializer for the 'Subject' model
    """

    programme_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['ID', 'Name', 'TotalQuestionsToSelect', 'programme_name']

    def get_programme_name(self, obj):
        """
        Custom serializer method to retrieve the 'Name' attribute of the related 'Programme'
        object associated with the 'Subject'

        Parameters:
            obj: The 'Subject' instance being serialized

        Returns:
            str: The 'Name' attribute of the associated 'Programme' object
        """

        return obj.ProgrammeID.Name


class QuestionProgrammesSerializers(serializers.ModelSerializer):
    """
    Serializes Programme model data for question-related operations
    """

    class Meta:
        model = Programme
        fields = ['ID', 'Name', 'TotalQuestions']


class QuestionProgrammesSubjectsSerializers(serializers.ModelSerializer):
    """
    Serializes the 'Subject' model for use in the QuestionProgrammes API
    """

    class Meta:
        model = Subject
        fields = ['ID', 'Name', 'TotalQuestions']


class QuestionSerializers(serializers.ModelSerializer):
    """
    Serializer class for converting Questions model instances to JSON format

    Attributes:
        Options: A serialized field representing the options for a question
        Subject: A serialized field representing the subject of a question
        Programme: A serialized field representing the program associated with the subject

    Methods:
        get_Programme(obj): Custom method to retrieve the program name associated with the question's subject
        get_Subject(obj): Custom method to retrieve the subject name associated with the question
        get_Options(obj): Custom method to retrieve a list of options for the question
    """

    Options = serializers.SerializerMethodField()
    Subject = serializers.SerializerMethodField()
    Programme = serializers.SerializerMethodField()

    class Meta:
        model = Questions
        fields = ['ID', 'Title', 'Answer', 'Subject', 'Programme', 'Options']

    def get_Programme(self, obj):
        """
        Retrieve the program name associated with the question's subject
        """
        return obj.SubjectID.ProgrammeID.Name

    def get_Subject(self, obj):
        """
        Retrieve the subject name associated with the question
        """

        return obj.SubjectID.Name

    def get_Options(self, obj):
        """
        Retrieve a list of options for the question
        """

        return [obj.OptionOne, obj.OptionTwo, obj.OptionThree, obj.OptionFour]


class ReportSerializers(serializers.ModelSerializer):
    """
    Serializer for converting ReportQuestion instances to JSON format

    Attributes:
        User: A serialized representation of the associated user's email
        Date: A serialized representation of the date formatted as '%b %d, %Y'
        Question: A serialized representation of the associated question's title

    Methods:
        get_User(obj): Custom method to retrieve the email of the associated user
        get_Date(obj): Custom method to format and retrieve the date in '%b %d, %Y' format
        get_Question(obj): Custom method to retrieve the title of the associated question
    """

    User = serializers.SerializerMethodField()
    Date = serializers.SerializerMethodField()
    Question = serializers.SerializerMethodField()

    class Meta:
        model = ReportQuestion
        fields = ['ID', 'User', 'Issue', 'Question', 'Date', 'IsMarked', 'QuestionID']

    def get_User(self, obj):
        """
        Custom method to retrieve the email of the associated user

        Args:
            obj: The ReportQuestion instance

        Returns:
            str: The email of the associated user
        """

        return obj.UserID.email

    def get_Date(self, obj):
        """
        Custom method to format and retrieve the date in '%b %d, %Y' format

        Args:
            obj: The ReportQuestion instance

        Returns:
            str: The formatted date string
        """

        return datetime.datetime.strptime(str(obj.Date), '%Y-%m-%d').strftime('%b %d, %Y')

    def get_Question(self, obj):
        """
        Custom method to retrieve the title of the associated question

        Args:
            obj: The ReportQuestion instance

        Returns:
            str: The title of the associated question
        """

        return obj.QuestionID.Title


class FeedbackSerializers(serializers.ModelSerializer):
    """
    Serializes the Feedback model for data representation

    This serializer is designed to convert instances of the Feedback model
    into a format that can be easily rendered into JSON or other content types

    Attributes:
        model (class): The Feedback model class that the serializer is based on
        fields (list): The specific fields from the Feedback model to include
                       in the serialized representation
    """

    Date = serializers.SerializerMethodField()

    class Meta:
        model = FeedBack
        fields = ['ID', 'Name', 'Email', 'Message', 'Date']

    def get_Date(self, obj):
        """
        Returns the formatted date and time for the provided Feedback instance

        Args:
            obj: The Feedback instance for which the date and time should be formatted

        Returns:
            str: The formatted date and time string (e.g., 'Jan 01, 2022 12:30:45 PM')
        """

        return datetime.datetime.strptime(str(obj.Date), "%Y-%m-%d %H:%M:%S.%f%z").strftime('%b %d, %Y %I:%M:%S %p')

class HistorySerializers(serializers.ModelSerializer):
    """
    Serializer for transforming Exam model instances into JSON format with additional fields

    Attributes:
        mark: A SerializerMethodField that represents the 'mark' field in the serialized output
        Program: A SerializerMethodField that represents the 'Program' field in the serialized output

    Methods:
        get_mark(obj): Custom method to retrieve the value for the 'mark' field in the serialized output
        get_Program(obj): Custom method to retrieve the value for the 'Program' field in the serialized output
    """

    mark = serializers.SerializerMethodField()
    Program = serializers.SerializerMethodField()

    class Meta:
        model = Exams
        fields = ['Date', 'Slug', 'mark', 'Program']

    def get_mark(self, obj):
        """
        Retrieve the value for the 'mark' field in the serialized output

        Parameters:
            obj: Exam model instance.

        Returns:
            The value of the 'CorrectCounter' field from the Exam model instance
        """

        return obj.CorrectCounter

    def get_Program(self, obj):
        """
        Retrieve the value for the 'Program' field in the serialized output

        Parameters:
            obj: Exam model instance.

        Returns:
            The value of the 'ProgrammeName' field from the Exam model instance
        """

        return obj.ProgrammeName
