from google.cloud import storage

muffato_stores_names = {
    '3_7': '37_MAX-TIRADENTES',
    '3_8': '32_OLARIAS',
    '3_11': '6_PORTAO',
    '3_13': '4_JOAO-PAULINO',
    '3_14': '81_AV-SAO-PAULO',
    '3_15': '48_IBIPORA',
    '3_16': '9_REP-ARGENTINA',
    '3_17': '76_MAX-CAMPO-COMPRIDO',
    '3_18': '86_MAX-FOZ-277',
    '3_19': '7_PQ-SAO-PAULO',
    '3_20': '18_BOICY',
    '3_21': '23_PORTINARI',
    '3_22': '25_MAX-DEBRET',
    '3_23': '26_PARANA',
    '3_24': '27_COMERCIAL',
    '3_25': '28_CAMPO-MOURAO',
    '3_26': '29_QUINTINO',
    '3_27': '30_DUQUE',
    '3_28': '33_BRASIL',
    '3_29': '35_SAUL',
    '3_30': '36_PRES-PRUDENTE',
    '3_31': '38_NOVA-RUSSIA',
    '3_32': '39_SAO-JOSE',
    '3_33': '44_MADRE-LEONIA',
    '3_34': '45_VILA-HAUER',
    '3_35': '47_CELSO-GARCIA',
    '3_36': '49_CERRO-AZUL',
    '3_37': '50_MAX-PRUDENTE',
    '3_38': '51_PARIGOT',
    '3_39': '53_TARUMA',
    '3_40': '54_CATARATAS',
    '3_41': '55_AEROPORTO',
    '3_42': '56_ALB-FOLLONI',
    '3_43': '57_REGIAO-NORTE',
    '3_44': '58_MARIPA',
    '3_45': '59_SAWADE',
    '3_46': '60_APUCARANA',
    '3_47': '61_PARANAVAI',
    '3_48': '63_VILA-A',
    '3_49': '64_REGIAO-SUL',
    '3_50': '65_MAX-COLOMBO',
    '3_51': '66_MAX-SAO-CRISTOVAO',
    '3_52': '67_MAX-PARANAGUA',
    '3_53': '68_UVARANAS',
    '3_54': '69_ARACATUBA',
    '3_55': '70_MAX-LINHA-VERDE',
    '3_56': '71_SJ-RIO-PRETO',
    '3_57': '72_AURORA',
    '3_58': '73_MAX-POTIRENDABA',
    '3_59': '74_NORTE-SHOPPING',
    '3_60': '75_MAX-BAIRRO-ALTO',
    '3_61': ['79_MAX-S╟ƒO-JOSE-PINHAIS', '79_MAX-SÃO-JOSE-PINHAIS'],
    '3_62': '80_BIRIGUI',
    '3_63': '82_CATUAI',
    '3_64': '83_JK',
    '3_65': '84_MAX-ZONA-NORTE-SJRP',
    '3_66': '85_MAX-ARAPONGAS',
    '3_67': '90_MAX-FRG',
    '3_68': '91_MAX-ARAUCARIA',
    '3_69': '89_MAX-PINHAIS',
    '3_70': '92_MAX-PONTA-GROSSA',
    '3_72': '98_VOTUPORANGA',
    '3_73': '96_SANTA-FELICIDADE',
    '3_77': '97_MAX-CATANDUVA',
    '3_78': '94_MAX-TITO-MUFFATO',
    '3_79': '99_SJRP-DAHMA',
    '3_80': '100_CATANDUVA'
}

muffato_dirs = {
    'mediar-painel': [
        'assortment',
        'muffato_product_base',
        'sales-raw',
        'transactions'
    ],
    'mediar-ftp': [
        'muffato'
    ]
}


class MuffatoFileAudit:
    def __init__(self, bucket, date):
        self.project_name = 'mediar-painel'
        self.date = date
        self.bucket = bucket

    def ftp_files(self):
        return

    def files_exist(self, file):
        client = storage.Client(self.project_name)
        bucket = client.get_bucket(self.bucket)
        blob = bucket.blob(file)
        return blob.exists()

    def unusual_files(self):
        return

    def check_for_small_file(self):
        return
