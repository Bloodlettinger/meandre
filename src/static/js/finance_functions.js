function add_finance_events(){

	if( jQuery('input.transaction_types_radio:checked').val() != 3 ){
		jQuery('#FinanceTransactionTargetWallet').parent().hide();
		jQuery('#FinanceTransactionExchangeRate').parent().hide();
	}else{
	
		if( current_wallet == $('#FinanceTransactionTargetWallet').val() ){
			another_wallet = $('#FinanceTransactionSourceWallet').val();
		}else{
			another_wallet = $('#FinanceTransactionTargetWallet').val();
		}
		
		if( currency_wallets[ current_wallet ] != currency_wallets[ another_wallet ] ){
			jQuery('#FinanceTransactionExchangeRate').parent().show();
		}else{
			jQuery('#FinanceTransactionExchangeRate').parent().hide();
		}
	}
	
	jQuery('input.transaction_types_radio').change(function(){
		if( jQuery(this).val() == 3 ){
			jQuery('#FinanceTransactionTargetWallet').parent().show(); 
			if( currency_wallets[ current_wallet ] != currency_wallets[ $('#FinanceTransactionTargetWallet').val() ] ){
				jQuery('#FinanceTransactionExchangeRate').parent().show();
			}else{
				jQuery('#FinanceTransactionExchangeRate').parent().hide();
			}
		}else{
			jQuery('#FinanceTransactionTargetWallet').parent().hide();
			jQuery('#FinanceTransactionExchangeRate').parent().hide();
		}
	});
	
	jQuery('#FinanceTransactionTargetWallet').change(function(){
		if( currency_wallets[ current_wallet ] != currency_wallets[ $(this).val() ] ){
			jQuery('#FinanceTransactionExchangeRate').parent().show();
		}else{
			jQuery('#FinanceTransactionExchangeRate').parent().hide();
		}
	});

}