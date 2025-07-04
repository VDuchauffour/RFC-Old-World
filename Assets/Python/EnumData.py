from Enum import IntEnum


class Region(IntEnum):
    ICELAND = 0
    THE_ISLES = 1
    THE_HIGHLANDS = 2
    THE_LOWLANDS = 3
    ULSTER = 4
    CONNAUGHT = 5
    LEINSTER = 6
    MUNSTER = 7
    NORTHUMBRIA = 8
    MIDLANDS = 9
    WALES = 10
    EAST_ANGLIA = 11
    KENT_ESSEX = 12
    WESSEX = 13
    CORNWALL_DEVON = 14
    VESTLANDET = 15
    TRONDELAG = 16
    JAMTLAND = 17
    NORRLAND = 18
    SVEALAND = 19
    OSTLANDET = 20
    GOTALAND = 21
    SCANIA = 22
    GOTLAND = 23
    DENMARK = 24
    FINLAND = 25
    KARELIA = 26
    ONEGA = 27
    DVINA = 28
    VOLGA = 29
    MOLOGA = 30
    NOVGOROD = 31
    INGRIA = 32
    PSKOV = 33
    VALDAI = 34
    TVER = 35
    MOSKVA = 36
    SUZDAL = 37
    RYAZAN = 38
    VORONEZH = 39
    OKA_DESNA_UPLANDS = 40
    SMOLENSK = 41
    WHITE_RUS = 42
    MSTISLAW = 43
    LATGALIA = 44
    LIVLAND = 45
    ESTONIA = 46
    COURLAND = 47
    SAMOGITIA = 48
    LITHUANIA = 49
    PRUSSIA = 50
    BLACK_RUS = 51
    POLESSIA = 52
    SEVERIA = 53
    SLOBODA_UKRAINE = 54
    DON = 55
    UKRAINE = 56
    ZAPOROGIA = 57
    TAURIA = 58
    AZOV = 59
    KUBAN = 60
    CAUCASUS_COAST = 61
    CRIMEA = 62
    KIEV = 63
    VOLHYNIA = 64
    PODLACHIA = 65
    MAZOVIA = 66
    SLESWICK = 67
    HOLSTEIN = 68
    MECKLENBURG = 69
    POMERANIA = 70
    POMERELIA = 71
    BREMEN_FRISIA = 72
    EASTPHALIA = 73
    BRANDEBURG = 74
    GREATER_POLAND = 75
    WESTPHALIA = 76
    HESSE = 77
    THURINGIA = 78
    MEISSEN_LUSATIA = 79
    SILESIA = 80
    RHINELAND = 81
    PALATINATE = 82
    FRANCONIA = 83
    SWABIA = 84
    BAVARIA = 85
    BOHEMIA = 86
    MORAVIA = 87
    AUSTRIA = 88
    UPPER_HUNGARY = 89
    LESSER_POLAND = 90
    GALICIA = 91
    PODOLIA = 92
    MOLDOVIA = 93
    YEDISAN = 94
    BUDJAK = 95
    DOBRUDJA = 96
    TRANSYLVANIA = 97
    WALLACHIA = 98
    HUNGARY = 99
    PANNONIA = 100
    BANAT = 101
    SYRMIA = 102
    CROATIA_SLAVONIA = 103
    ISTRIA = 104
    STYRIA_CARINTHIA = 105
    VENETO = 106
    DALMATIA = 107
    BOSNIA = 108
    RASCIA = 109
    TORLAKIA = 110
    MOESIA = 111
    THRACE = 112
    MACEDONIA = 113
    ALBANIA = 114
    EPIRUS = 115
    THESSALY = 116
    ATTICA = 117
    MOREA = 118
    IONIAN_ISLANDS = 119
    AEGEAN_ISLANDS = 120
    DARDANELLES = 121
    IONIA = 122
    RHODES = 123
    CRETE = 124
    BOSPORUS = 125
    BITHYNIA = 126
    PHRYGIA = 127
    LYCIA = 128
    PAMPHYLIA = 129
    LYCAONIA = 130
    GALATIA = 131
    PAPHLAGONIA = 132
    PONTUS = 133
    CHALDIA = 134
    CAPPADOCIA = 135
    ARMENIA = 136
    CILICIA = 137
    NORTHERN_SYRIA = 138
    ANTIOCH = 139
    SYRIA = 140
    ARABIA = 141
    LEBANON = 142
    HEJAZ = 143
    TRANSJORDAN = 144
    PALESTINE = 145
    CYPRUS = 146
    SINAI = 147
    LOWER_EGYPT = 148
    UPPER_EGYPT = 149
    CYRENAICA = 150
    TRIPOLITANIA = 151
    IFRIQIYA = 152
    BARBARY = 153
    MAURETANIA = 154
    RIF = 155
    FES = 156
    ATLANTIC_MOROCCO = 157
    SOUSS = 158
    MARRAKESH = 159
    ATLAS = 160
    CANARIES = 161
    MADEIRA = 162
    AZORES = 163
    MALTA = 164
    SICILY = 165
    CALABRIA = 166
    APULIA = 167
    CAMPANIA = 168
    MARCHE = 169
    LAZIO = 170
    TUSCANY = 171
    EMILIA_ROMAGNA = 172
    LIGURIA = 173
    PIEDMONT = 174
    LOMBARDY = 175
    VERONA = 176
    SARDINIA = 177
    TYROL = 178
    HELVETIA = 179
    ALSACE = 180
    LORRAINE = 181
    FRISIA = 182
    HOLLAND = 183
    BRABANT = 184
    WALLONIA = 185
    FLANDERS = 186
    PICARDY_ARTOIS = 187
    CHAMPAGNE = 188
    ILE_DE_FRANCE = 189
    NORMANDY = 190
    BRITTANY = 191
    POITOU = 192
    ANJOU = 193
    BERRY = 194
    BURGUNDY_FRANCHE_COMTE = 195
    SAVOY = 196
    LYONNAIS = 197
    AUVERGNE = 198
    GUYENNE = 199
    LANGUEDOC = 200
    DAUPHINY = 201
    PROVENCE = 202
    CORSICA = 203
    CATALONIA = 204
    ARAGON = 205
    NAVARRE = 206
    CANTABRIA = 207
    ASTURIAS = 208
    GALIZA = 209
    PORTUGAL = 210
    LUSITANIA = 211
    LEON = 212
    CASTILLE = 213
    LA_MANCHA = 214
    VALENCIA = 215
    EXTREMADURA = 216
    ANDALUSIA = 217
    MURICA = 218
    GRANADA = 219
    BALEARES = 220
    ROUSSILLON = 221
    SAHARA = 222


class Ocean(IntEnum):
    ATLANTIC = 223


class Sea(IntEnum):
    MEDITERRANEAN = 224
    RED = 225
    BALTIC = 226
    BLACK = 227
    AZOV = 228
    WHITE = 229


class Lake(IntEnum):
    SNAASAVATNET = 230
    KALLSJOEN = 231
    STROEMS_VATTUDAL = 232
    STORSJOEN = 233
    SILJAN = 234
    VAENERN = 235
    VAETTERN = 236
    HJAELMAREN = 237
    MAERLAEN = 238
    PYHAJARVI = 239
    LOHJANJARVI = 240
    LAPPAJARVI = 241
    NASIJARVI = 242
    VANAJAVESI = 243
    PAIJANNE = 244
    KEITELE = 245
    NILAKKA = 246
    ONKIVESI = 247
    LISVESI = 248
    PUULA = 249
    VUOHIJARVI = 250
    KYYVESI = 251
    KALLAVESI = 252
    SAIMAA = 253
    VIINIJARVI = 254
    ORIVESI = 255
    HOYTIAINEN = 256
    PIELINEN = 257
    KOITERE = 258
    LAGODA = 259
    SYAMOZERO = 260
    SEGOZERO = 261
    SANDAL = 262
    VYGOZERO = 263
    ONEGA = 264
    VOLDOZERO = 265
    LACHA = 266
    VOZHE = 267
    KUBENA = 268
    BELOYE = 269
    ILMEN = 270
    PIHKVA = 271
    PEIPUS = 272
    VORTSJARVI = 273
    SPIRDINGSE = 274
    LIMFJORD = 275
    NEAGH = 276
    LEMAN = 277
    BODENSE = 278
    GARDA = 279
    BALATON = 280
    SKADAR = 281
    OHRID = 282
    PRESPA = 283
    ASKANIA = 284
    AKROTIRI = 285
    KARALLIS = 286
    TATTA = 287
    GALILEE_SEA = 288
    DEAD_SEA = 289
    MOERIS = 290
    SALT_SEBKHA_OF_ORAN = 291
    SALT_CHOTT_ECH_CHERGUI = 292
    SALT_CHOTT_EL_HODNA = 293
    SALT_CHOTT_MELGHIR = 294
    SALT_CHOTT_EL_DEJRID = 295
