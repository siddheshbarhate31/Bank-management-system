from app import ma
from marshmallow.validate import Length, Regexp
from marshmallow import fields, INCLUDE

name_string = '^[a-zA-Z]*$'


class AccountTransactionDetailsSchema(ma.Schema):
    """Adding the Schema validations to the AccountTransactionDetails """
    transaction_amount = fields.Int(required=True)
    bank_account_id = fields.Int(required=True)
    transaction_type_id = fields.Int(required=True)
    fund_id = fields.Int(required=True)
    transaction_status = fields.String(required=True)

    class Meta:

        """ Exposed fields """

        fields = ('transaction_amount', 'transaction_date', 'bank_account_id', 'transaction_status',
                  'transaction_type_id', 'account_type_id', 'fund_id')


account_transaction_detail_schema = AccountTransactionDetailsSchema()
account_transaction_details_schema = AccountTransactionDetailsSchema(many=True)


class TransactionTypeSchema(ma.Schema):

    """Adding the Schema validations to the TransactionType """

    transaction_type = fields.String(required=True, validate=(Length(max=20), Regexp(name_string)))

    class Meta:

        """ Exposed fields """

        fields = ('id', 'transaction_type')
        unknown = INCLUDE
        load_instance = True


transaction_type_schema = TransactionTypeSchema()
transactions_type_schema = TransactionTypeSchema(many=True)


class FundTransferSchema(ma.Schema):

    """Adding the Schema validations to the FundTransfer """

    from_account = fields.Str(required=True, validate=Regexp("^[0-9]{10}$|^[0-9]{12}$"))
    to_account = fields.Str(validate=Regexp("^[0-9]{10}$|^[0-9]{12}$"))
    transaction_amount = fields.Int(required=True)

    class Meta:

        """ Exposed fields """

        fields = ('id', 'from_account', 'to_account', 'transaction_amount')
        unknown = INCLUDE
        load_instance = True


fund_transfer_schema = FundTransferSchema()
funds_transfer_schema = FundTransferSchema(many=True)
