from app import ma
from marshmallow.validate import Length
from marshmallow import fields, INCLUDE


class AccountTransactionDetailsSchema(ma.Schema):
    """Adding the Schema validations to the AccountTransactionDetails """
    transaction_amount = fields.Int(required=True)
    bank_account_id = fields.Int(required=True)
    transaction_type_id = fields.Int(required=True)
    fund_id = fields.Int(required=True)

    class Meta:

        """ Exposed fields """

        fields = ('transaction_amount', 'transaction_date', 'bank_account_id', 'transaction_type_id',
                  'account_type_id', 'fund_id')
        unknown = INCLUDE
        load_instance = True


account_transaction_detail_schema = AccountTransactionDetailsSchema()
account_transaction_details_schema = AccountTransactionDetailsSchema(many=True)


class TransactionTypeSchema(ma.Schema):

    """Adding the Schema validations to the TransactionType """

    transaction_type = fields.String(required=True, validate=Length(min=2, max=100))

    class Meta:

        """ Exposed fields """

        fields = ('id', 'transaction_type')
        unknown = INCLUDE
        load_instance = True


transaction_type_schema = TransactionTypeSchema()
transactions_type_schema = TransactionTypeSchema(many=True)


class FundTransferSchema(ma.Schema):

    """Adding the Schema validations to the FundTransfer """

    from_account = fields.Int(required=True)
    to_account = fields.Int(required=True)
    transaction_amount = fields.Int(required=True)

    class Meta:

        """ Exposed fields """

        fields = ('id', 'from_account', 'to_account', 'transaction_amount')
        unknown = INCLUDE
        load_instance = True


fund_transfer_schema = FundTransferSchema()
funds_transfer_schema = FundTransferSchema(many=True)
