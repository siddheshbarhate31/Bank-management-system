from app import ma
from marshmallow.validate import Length, Regexp
from marshmallow import fields
from app.model.user import User

name_string = '^[a-zA-Z]*$'
address_string = '^[a-zA-Z ]*$'


class UserSchema(ma.Schema):
    """Adding the Schema validations to the User """

    first_name = fields.Str(required=True, validate=(Length(max=50), Regexp(name_string)))
    last_name = fields.Str(required=True, validate=(Length(max=50), Regexp(name_string)))
    address = fields.Str(required=True, validate=(Length(max=100), Regexp(address_string)))
    mobile_number = fields.String(required=True, validate=(Regexp('^[789]\d{9}$'), Length(equal=10)))
    email_id = fields.Email(required=True, validate=Regexp('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'))
    password = fields.Str(required=True, validate=Regexp('[A-Za-z0-9@#$%^&+=]{8,}'))
    user_type_id = fields.Int(strict=True, required=True)

    class Meta:

        """ Exposed fields """

        fields = ('id', 'first_name', 'last_name', 'address', 'mobile_number', 'email_id', 'password',
                  'user_type_id', 'created_on')



def if_email_id_exist(email_id):
    return User.query.filter(User.email_id == email_id).first()


def if_mobile_no_exist(mobile_number):
    return User.query.filter(User.mobile_number == mobile_number).first()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserTypeSchema(ma.Schema):

    """Adding Schema validations to the UserType"""

    user_type = fields.Str(required=True, validate=(Length(max=20), Regexp(name_string)))

    class Meta:

        """Expose fields"""

        fields = ('id', 'user_type')


user_type_schema = UserTypeSchema()
users_type_schema = UserSchema(many=True)


