Drop table UFMT_CONVERSION_BK;
Create table UFMT_CONVERSION_BK as Select * from UFMT_CONVERSION;
Delete from UFMT_CONVERSION;

Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '1','0','Transaction to processing code' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '2','0','Account From/To' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '3','2','YYYYMMDD to YYMMDD' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '4','2','YYYYMMDD to MMDD' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '5','2','YYYYMMDD to YYYY' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '6','0','SOPP Response code conversion' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '7','2','Add leading zero to HHMMSS' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '8','2','Get first 17 from DE48 as Ledg Bal' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '9','2','Get second 17 from DE48 as NET Bal' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '10','2','Get sign from DE48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '11','4','Change sign' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '12','4','Multiple x2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '13','0','Transaction to MTI for DE56' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '14','0','ACQ. inst_id conversion for DE56' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '15','0','Transaction to processing code for Rever' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '16','0','Define 1 if reversal' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '17','0','ACQ. inst_id conversion for DE32' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '18','5','Custom Function get_fee_DE46' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '19','5','Custom Function setup_DE46' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '20','0','ACQ. inst_id conversion for DE67' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '21','5','Custom Function add_two_digit_size' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '22','5','Custom function get time' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '23','2','Cut track2 ; etc.' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '24','2','Get balance currency from DE48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '25','5','Custom function setup_de37_yddd' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '27','0','Processing code Flexcube' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '28','0','Flexcube Private data DE60' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '29','5','Custom Function setup_DE28' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '30','5','Custom Function get_balance_DE54' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '31','5','Custom Function process_mini_stmt' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '32','5','Custom Function set_network_code_DE67' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '33','0','Flexcube Response code conversion' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '34','0','Processing Code Flexcube BIN' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '35','5','Custom Function setup_DE116' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '36','5','Custom Function set_location_DE43' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '37','5','Custom Function format_track2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '38','2','Format value for F126' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '39','2','Get BIN from HPAN' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '40','0','BIN n currency -> GL account' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '41','0','TT n SI n CC -> GL account' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '42','0','Service ID to processing code for TT508' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '43','2','Trim to 12' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '44','0','Trans_type for sending F103 as GL acct' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '45','0','Value_id 175 -> false/true' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '46','0','Currency -> Credit card GL' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '47','0','(iss_inst,trx_curr)->THEMONUS GL' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '48','4','Change sign' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '49','2','Format 16 digit amounts' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '50','0','LOV for credit card BINs' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '51','0','LOV for TT/SI list used by cond 33' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '52','2','Get F11 from utrnno (last 6 digits)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '53','0','acq_inst,TT,CC -> USONTHEM GL account' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '54','0','LOV for TT/SI list used by cond 37' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '55','5','Custom Function setup_DE46_ACL_destfee' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '56','0','Value_id 175 -> 1/0, used by cond 41' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '57','0','Trans_type for sending F103 as Acct1' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '58','4','SVT_TXN_AMT_A1CUR-SVT_ISS_FEE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '59','0','SVT_NTWM_MSGTYPE to F70' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '60','0','Epayint prcode F3 mapping' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '61','5','Custom function for F125 from MB' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '62','0','MobileBankiing Response code conversion' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '63','0','SVT_NTWM_MSGTYPE to F70 (for NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '64','0','F70 to trans_type (for NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '65','0','To RC mapping (for NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '67','4','From F7 (MMDDhhmmss) to date (YYYYMMDD)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '68','1','MMDD to YYYYMMDD' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '69','1','YYYYMMDD to MMDD' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '70','2','Prcode->trans_type(NBC)(field extract)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '71','0','Prcode->trans_type(NBC)(mapping)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '72','2','F43 -> Name (NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '73','2','F43 -> City (NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '74','2','F43 -> Country (NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '75','0','Trans_type to prcode ( NBC) ' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '76','0','MCC to terminal type (NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '77','0','TT for sending F11 T24 as SV_TRACE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '78','5','Custom function build_mini_statment_nbc' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '79','0','Prcode->fintran(NBC)(mapping)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '80','2','Prcode->fintran(NBC)(field extract)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '81','0','Currency -> Cardless CWD GL' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '82','0','ReceiveID -> BANK_ID2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '83','5','Custom function set_rout_by_bankid' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '84','2','F48 -> NBC IBFT BNB ACC_TP' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '85','2','F48 -> NBC IBFT BNB BNK_CODE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '86','2','F48 -> NBC IBFT BNB BNK_NAME' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '87','2','F48 -> NBC IBFT BNB ACC_NO' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '88','2','F48 -> NBC IBFT BNB ACC_NAME' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '89','2','F48 -> NBC IBFT BNB AMOUNT' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '90','0','COND CONV: NBC IBFT trans_type' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '91','0','BANK_ID2->ReceiveID (NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '92','0','BANK_ID2->Bank name (NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '93','2','NBC IBFT BNB ACC_TP->F48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '94','2','NBC IBFT BNB BNK_CODE->F48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '95','2','NBC IBFT BNB BNK_NAME->F48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '96','2','NBC IBFT BNB ACC_NO->F48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '97','2','NBC IBFT BNB ACC_NAME->F48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '98','2','NBC IBFT BNB AMOUNT->F48' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '99','0','Set TT to 621' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '100','5','Custom function ufmt_check_mac' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '101','5','Custom function ufmt_generate_mac' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '102','2','Format fee value ( add leading zeroes )' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '103','4','NBC Total fee calculation' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '104','4','NBC Total fee calculation (from local)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '105','4','NBC SET_CARD_DATA_INPUT_MODE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '106','0','NBC SET_CARD_DATA_INPUT_MODE_2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '107','4','NBC SET_PIN_CAPTURE_CAPABILITY' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '108','0','NBC SET_PIN_CAPTURE_CAPABILITY_2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '109','0','NBC SET_CARDHOLDER_PRESENCE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '110','0','NBC SET_CARD_PRESENCE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '111','4','NBC SET POS DATA CODE' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '112','4','NBC Total fee calculation - 2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '113','4','NBC Total fee calculation - 3' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '114','4','NBC Total fee calculation (from local)-2' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '115','4','NBC Total fee calculation (from local)-3' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '116','0','TT for sending NBC F28' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '117','0','From RC mapping (for NBC)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '118','0','Set BANK_ID to 99999' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '119','0','Set BANK_ID to 99998' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '120','0','Set TT to 777' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '121','2','NBC Orig MTI->F90' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '122','2','NBC Orig F11->F90' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '123','2','NBC Orig F7->F90' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '124','2','NBC Orig F32->F90' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '125','2','NBC Orig F33->F90' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '126','4','NBC Set Orig Data Element' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '127','0','Set to 0' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '128','0','T24 NSS TT->prcode' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '129','4','T24 NSS settlement amt calculation' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '130','0','sign mapping (- -> -1,+ -> 1)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '131','4','Multiple with local amount sign' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '132','0','NBC ISS2_INST->orig_prcode(IBFT PIN)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '133','4','T24 NSS Set F56' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '134','0','Set to TT 794' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '135','0','T24 NSS TT->prcode (THEMONUS)' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '136','4','Request_amt - acq_fee' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '137','0','COND CONV: TT for sending NBC F54' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '138','5','Cust func set_matching_key_from_src' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '139','5','Cust func find_orig_ufmt_utrnno_by_key' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '140','4','NBC set orig key data' );
Insert into UFMT_CONVERSION ( CONV_KEY,CONV_TYPE,DESCRIPTION ) Values ( '141','4','NBC set orig utrnno' );

COMMIT;
