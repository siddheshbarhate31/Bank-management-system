from app import ma
from marshmallow.validate import Length, Range, Regexp
from marshmallow import fields
from random import randint

name_string = '^[a-zA-Z]*$'
address_string = '^[a-zA-Z ]*$'


class BankAccountSchema(ma.Schema):
    """Adding the Schema validations to the BankAccount """
    user_id = fields.Int(strict=True, required=True)
    account_type_id = fields.Int(strict=True, required=True)
    branch_id = fields.Int(strict=True, required=True)
    balance = fields.Int(strict=True, required=True, validate=Range(min=1000, max=50000))

    class Meta:

        """ Exposed fields """

        fields = ('account_number', 'is_active', 'deleted', 'balance', 'user_id', 'account_type_id', 'branch_id',
                  'created_on', 'balance')
        load_instance = True


bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many=True)


def generate_random_number(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class AccountTypeSchema(ma.Schema):
    """Adding the Schema validations to the AccountType """

    account_type = fields.String(required=True, validate=(Length(max=20), Regexp(name_string)))

    class Meta:

        """ Exposed fields """

        fields = ('id', 'account_type')
        load_instance = True


account_type_schema = AccountTypeSchema()
accounts_type_schema = AccountTypeSchema(many=True)


class BranchDetailsSchema(ma.Schema):
    """Adding the Schema validations to the BranchDetails """

    branch_name = fields.Str(required=True, validate=(Length(max=100), Regexp('^[a-zA-Z ]*$')))
    branch_address = fields.Str(required=True, validate=(Length(max=100), Regexp('^[a-zA-Z ]*$')))

    class Meta:

        """ Exposed fields """

        fields = ('branch_id', 'branch_name', 'branch_address')
        load_instance = True


branch_detail_schema = BranchDetailsSchema()
branch_details_schema = BranchDetailsSchema(many=True)
