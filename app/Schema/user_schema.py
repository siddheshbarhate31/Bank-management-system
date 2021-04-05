from app import ma
from marshmallow.validate import Length, Regexp
from marshmallow import fields, INCLUDE


class UserSchema(ma.Schema):
    """Adding the Schema validations to the User """

    first_name = fields.Str(required=True, validate=Length(min=2, max=100))
    last_name = fields.Str(required=True, validate=Length(min=2, max=100))
    address = fields.Str(required=True, validate=Length(min=2, max=100))
    mobile_number = fields.Str(required=True, validate=Length(min=10))
    email_id = fields.Email(required=True, validate=Regexp('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'))
    password = fields.Str(required=True, validate=Length(min=5, max=100))
    user_type_id = fields.Int(required=True)

    class Meta:

        """ Exposed fields """

        fields = ('id', 'first_name', 'last_name', 'address', 'mobile_number', 'email_id', 'password',
                  'user_type_id', 'created_on')
        unknown = INCLUDE
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserTypeSchema(ma.Schema):

    """Adding Schema validations to the UserType"""

    user_type = fields.Str(required=True, validate=Length(max=20))

    class Meta:

        """Expose fields"""

        fields = ('id', 'user_type')


user_type_schema = UserTypeSchema()
users_type_schema = UserSchema(many=True)


