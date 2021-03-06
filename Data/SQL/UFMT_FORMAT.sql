Drop table UFMT_FORMAT_BK;
Create table UFMT_FORMAT_BK as Select * from UFMT_FORMAT;
Delete from UFMT_FORMAT;

Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1','2','iBSM CBS Format - DE 54','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '2','2','iBSM CBS Format - DE 54 sub-record','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '100','0','iBSM CBS Format - Out 0800','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '101','0','iBSM CBS Format - In 0810','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '102','0','iBSM CBS Format - In 0800','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '103','0','iBSM CBS Format - Out 0810','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '200','0','iBSM CBS Format - Out 0200','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '201','0','iBSM CBS Format - In 0210','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '300','0','iBSM CBS Format - Out 0400/0420','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '301','0','iBSM CBS Format - In 0410/0430','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '302','0','iBSM CBS Format - Out 0420','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '303','0','iBSM CBS Format - In 0430','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '400','2','CMS-TRX Format - Header','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '402','2','CMS-TRX Format - In Request','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '403','2','CMS-TRX Format - Out Response','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '404','2','CMS-TRX Transfer ExtraData Request','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '405','2','CMS-TRX Transfer ExtraData Response','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1100','0','Xlink Format - Out 0800','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1101','0','Xlink Format - In 0810','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1102','0','Xlink Format - In 0800','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1103','0','Xlink Format - Out 0810','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1200','0','Xlink Format - Out 0200','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1201','0','Xlink Format - In 0210','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1300','0','Xlink Format - Out 0600','1' );
Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( '1301','0','Xlink Format - In 0610','1' );

COMMIT;
