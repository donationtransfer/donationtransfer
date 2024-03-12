class Config:
    SECRET_KEY = '1dba72f145fedbdab39251c523cf52ba'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQL_SERVER = 'donation.database.windows.net'
    SQL_USERNAME = 'shurukn'
    SQL_PASSWORD = 'Fr4ngine!'
    SQL_DATABASE = 'user'
    SQL_PORT = 1433
    SQL_AUTHENTICATION_CONNECTION_STRING = f'Server=tcp:{app.config["SQL_SERVER"]},{app.config["SQL_PORT"]};Initial Catalog={app.config["SQL_DATABASE"]};Persist Security Info=False;User ID={app.config["SQL_USERNAME"]};Password={app.config["SQL_PASSWORD"]};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
    SQL_DRIVER = '{ODBC Driver 17 for SQL Server}'
    db_connection = connect(host=f"{app.config['SQL_SERVER']}", user=f"{app.config['SQL_USERNAME']}", passwd=f"{app.config['SQL_PASSWORD']}", database=f"{app.config['SQL_DATABASE']}")
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{app.config['SQL_USERNAME']}:{app.config['SQL_PASSWORD']}>@{app.config['SQL_SERVER']}/{app.config['SQL_DATABASE']}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AZURE_CLIENT_ID = 'a5d33a9f-0fca-4218-a9ec-79dfa26af34c'
    AZZURE_SUBSCRIPTION_ID = 'e026e436-3a12-4d02-a3a6-755668fc583d'
    ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/gif'}
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'shuryukn@donationtransfer.com'
    MAIL_PASSWORD = 'Fr4ngine!'
    MAIL_DEFAULT_SENDER = 'shurukn'
    COUNTRIES = {
       "Argentina": {"currency": "ARS", "symbol": "$", "phone_code": "+54", "value": 0.001181},
       "Australia": {"currency": "AUD", "symbol": "A$", "phone_code": "+61", "value": 0.663143},
       "Bahrain": {"currency": "BHD", "symbol": ".د.ب", "phone_code": "+973", "value": 2.659574},
       "Botswana": {"currency": "BWP", "symbol": "P", "phone_code": "+267", "value": 0.072855},
       "Brazil": {"currency": "BRL", "symbol": "R$", "phone_code": "+55", "value": 0.200780},
       "Brunei": {"currency": "BND", "symbol": "$", "phone_code": "+673", "value": 0.751080},
       "Bulgaria": {"currency": "BGN", "symbol": "лв", "phone_code": "+359", "value": 0.558317},
       "Canada": {"currency": "CAD", "symbol": "$", "phone_code": "+1", "value": 0.741714},
       "Chile": {"currency": "CLP", "symbol": "$", "phone_code": "+56", "value": 0.001040},
       "China": {"currency": "CNY", "symbol": "¥", "phone_code": "+86", "value": 0.139169},
       "Colombia": {"currency": "COP", "symbol": "$", "phone_code": "+57", "value": 0.000256},
       "Czech Republic": {"currency": "CZK", "symbol": "Kč", "phone_code": "+420", "value": 0.043219},
       "Denmark": {"currency": "DKK", "symbol": "kr", "phone_code": "+45", "value": 0.146723},
       "Eurozone": {"currency": "EUR", "symbol": "€", "phone_code": "Varies", "value": 1.091973},
       "Hong Kong": {"currency": "HKD", "symbol": "$", "phone_code": "+852", "value": 0.127869},
       "Hungary": {"currency": "HUF", "symbol": "Ft", "phone_code": "+36", "value": 0.002776},
       "Iceland": {"currency": "ISK", "symbol": "kr", "phone_code": "+354", "value": 0.007342},
       "India": {"currency": "INR", "symbol": "₹", "phone_code": "+91", "value": 0.012087},
       "Indonesia": {"currency": "IDR", "symbol": "Rp", "phone_code": "+62", "value": 0.000064},
       "Iran": {"currency": "IRR", "symbol": "﷼", "phone_code": "+98", "value": 0.000024},
       "Israel": {"currency": "ILS", "symbol": "₪", "phone_code": "+972", "value": 0.279663},
       "Japan": {"currency": "JPY", "symbol": "¥", "phone_code": "+81", "value": 0.006801},
       "Kazakhstan": {"currency": "KZT", "symbol": "₸", "phone_code": "+7", "value": 0.002245},
       "Kuwait": {"currency": "KWD", "symbol": "KD", "phone_code": "+965", "value": 3.246847},
       "Libya": {"currency": "LYD", "symbol": "ل.د", "phone_code": "+218", "value": 0.208164},
       "Malaysia": {"currency": "MYR", "symbol": "RM", "phone_code": "+60", "value": 0.213505},
       "Mauritius": {"currency": "MUR", "symbol": "₨", "phone_code": "+230", "value": 0.021858},
       "Mexico": {"currency": "MXN", "symbol": "$", "phone_code": "+52", "value": 0.059444},
       "Nepal": {"currency": "NPR", "symbol": "₨", "phone_code": "+977", "value": 0.007551},
       "New Zealand": {"currency": "NZD", "symbol": "$", "phone_code": "+64", "value": 0.617507},
       "Norway": {"currency": "NOK", "symbol": "kr", "phone_code": "+47", "value": 0.096082},
       "Oman": {"currency": "OMR", "symbol": "ر.ع.", "phone_code": "+968", "value": 2.596717},
       "Pakistan": {"currency": "PKR", "symbol": "₨", "phone_code": "+92", "value": 0.003584},
       "Philippines": {"currency": "PHP", "symbol": "₱", "phone_code": "+63", "value": 0.017991},
       "Poland": {"currency": "PLN", "symbol": "zł", "phone_code": "+48", "value": 0.254667},
       "Qatar": {"currency": "QAR", "symbol": "ر.ق", "phone_code": "+974", "value": 0.274725},
       "Romania": {"currency": "RON", "symbol": "lei", "phone_code": "+40", "value": 0.219244},
       "Russia": {"currency": "RUB", "symbol": "₽", "phone_code": "+7", "value": 0.011006},
       "Saudi Arabia": {"currency": "SAR", "symbol": "ر.س", "phone_code": "+966", "value": 0.266667},
       "Singapore": {"currency": "SGD", "symbol": "S$", "phone_code": "+65", "value": 0.751080},
       "South Africa": {"currency": "ZAR", "symbol": "R", "phone_code": "+27", "value": 0.053418},
       "South Korea": {"currency": "KRW", "symbol": "₩", "phone_code": "+82", "value": 0.000759},
       "Sri Lanka": {"currency": "LKR", "symbol": "Rs", "phone_code": "+94", "value": 0.003254},
       "Sweden": {"currency": "SEK", "symbol": "kr", "phone_code": "+46", "value": 0.097899},
       "Switzerland": {"currency": "CHF", "symbol": "CHF", "phone_code": "+41", "value": 1.139420},
       "Taiwan": {"currency": "TWD", "symbol": "NT$", "phone_code": "+886", "value": 0.031790},
       "Thailand": {"currency": "THB", "symbol": "฿", "phone_code": "+66", "value": 0.028257},
       "Trinidad and Tobago": {"currency": "TTD", "symbol": "TT$", "phone_code": "+1-868", "value": 0.147319},
       "Turkey": {"currency": "TRY", "symbol": "₺", "phone_code": "+90", "value": 0.031401},
       "Ukraine": {"currency": "UAH", "symbol": "₴", "phone_code": "+380", "value": 0.027054},  # Estimated value
       "United Arab Emirates": {"currency": "AED", "symbol": "د.إ", "phone_code": "+971", "value": 0.272294},
       "United Kingdom": {"currency": "GBP", "symbol": "£", "phone_code": "+44", "value": 1.285207},
       "United States": {"currency": "USD", "symbol": "$", "phone_code": "+1", "value": 1},
       "Uruguay": {"currency": "UYU", "symbol": "$U", "phone_code": "+598", "value": 0.022463},  # Estimated value
       "Venezuela": {"currency": "VES", "symbol": "Bs.", "phone_code": "+58", "value": 0.0000001},  # Hyperinflation context, actual value may vary significantly
       "Vietnam": {"currency": "VND", "symbol": "₫", "phone_code": "+84", "value": 0.000043},
       "Yemen": {"currency": "YER", "symbol": "﷼", "phone_code": "+967", "value": 0.004001},
      }
