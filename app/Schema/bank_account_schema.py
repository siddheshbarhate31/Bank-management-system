from app import ma
from marshmallow import fields, INCLUDE


class BankAccountSchema(ma.Schema):
    """Adding the Schema validations to the BankAccount """

    account_number = fields.Int(required=True)
    is_active = fields.Boolean(required=True)
    deleted = fields.Boolean(required=True)
    user_id = fields.Boolean(required=True)
    account_type_id = fields.Int(required=True)
    branch_id = fields.Int(required=True)

    class Meta:

        """ Exposed fields """

        fields = ('account_number', 'is_active', 'deleted', 'user_id', 'account_type_id', 'branch_id')
        unknown = INCLUDE
        load_instance = True


bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many=True)
