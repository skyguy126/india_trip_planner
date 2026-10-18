from pathlib import Path
import re,json,os
ROOT=Path(__file__).parent
bank=(ROOT/'data'/'destination_bank.md').read_text()
# id | lat | lon | gateway | regional access hours | suggested on-site hours
raw='''
1|32.2432|77.1892|MAN|0|16
2|32.1157|77.1733|MAN|1|6
3|32.4706|77.1256|MAN|2|8
4|32.2495|77.2210|MAN|1|40
5|31.6460|77.3760|MAN|3|16
6|31.5900|77.3500|MAN|3|16
7|31.7380|77.3790|MAN|3|12
8|32.0397|76.7217|DHM|2|12
9|32.0410|76.8450|DHM|3|16
10|32.2190|76.3234|DHM|.5|16
11|32.1100|76.5360|DHM|1|8
12|31.7540|77.1010|MAN|3|8
13|32.0100|77.3150|MAN|2|16
14|31.1048|77.1734|IXC|3.5|12
15|30.9680|77.1970|IXC|3.5|6
16|31.2570|77.4610|IXC|5|12
17|31.5370|78.2760|IXC|10|24
18|32.2270|78.0710|IXC|18|32
19|32.5720|77.0240|MAN|4|16
20|32.5530|76.1260|DHM|5|16
21|34.0837|74.7973|SXR|.75|16
22|34.0484|74.3805|SXR|2|16
23|34.0161|75.3140|SXR|2.5|16
24|34.3000|75.2920|SXR|3|8
25|33.8990|74.6630|SXR|2|8
26|34.5930|74.8300|SXR|7|24
27|33.0830|75.3260|IXJ|3|16
28|34.1526|77.5771|IXL|.5|24
29|34.5440|77.5690|IXL|5|16
30|33.9100|78.4600|IXL|6|12
31|32.9090|78.3240|IXL|7|16
32|32.7900|78.9650|IXL|8|16
33|34.2820|76.7740|IXL|4|12
34|33.4650|76.8850|IXL|12|32
35|33.9820|77.4340|IXL|3|40
36|30.0869|78.2676|DED|.75|16
37|30.1360|78.3900|DED|1.5|8
38|29.9457|78.1642|DED|1.25|8
39|30.1460|78.5980|DED|3|5
40|30.4890|79.1860|DED|7|16
41|30.7352|79.0669|DED|8|24
42|30.7440|79.4920|DED|10|16
43|30.5290|79.5660|DED|9|16
44|31.0380|78.7370|DED|8|16
45|30.8380|78.5640|DED|9|32
46|31.0790|78.1800|DED|10|40
47|30.0710|80.2380|KGM|10|24
48|29.6430|79.7560|KGM|4|16
49|29.3480|79.5520|KGM|1.5|12
50|29.3950|79.1260|KGM|2|16
51|30.7270|79.6050|DED|10|40
52|31.6340|74.8723|ATQ|.5|16
53|31.2390|76.5020|IXC|2|8
54|25.3176|82.9739|VNS|.75|16
55|25.3810|83.0210|VNS|1|6
56|27.1767|78.0081|AGR|.5|12
57|26.8467|80.9462|LKO|.5|12
58|27.5650|77.6590|AGR|1.5|12
59|28.6139|77.2090|DEL|0|16
60|25.2570|91.7320|SHL|2.5|4
61|25.2610|91.7110|SHL|2.5|5
62|25.3480|92.5100|SHL|5|16
63|25.2480|91.6760|SHL|3|12
64|25.2760|91.7080|SHL|2.5|8
65|25.2060|92.0110|SHL|3|8
66|25.3310|91.8900|SHL|2|8
67|25.3260|91.8540|SHL|2|5
68|25.4410|92.2050|SHL|2.5|8
69|25.2670|90.5200|GAU|9|16
70|25.3510|90.6980|GAU|8|24
71|25.5788|91.8933|SHL|0|12
72|25.7170|91.4710|SHL|3|12
73|26.5775|93.1711|GAU|5|24
74|26.7260|91.0270|GAU|4|24
75|26.9510|94.2190|JRH|2.5|16
76|27.4728|94.9120|DIB|.5|12
77|26.1445|91.7362|GAU|.5|12
78|26.2340|92.0500|GAU|2|8
79|27.5800|95.3800|DIB|2|16
80|27.2720|95.3310|DIB|2|16
81|25.1667|93.0167|LMG|4|16
82|26.9840|94.6370|DIB|2.5|8
83|27.3600|92.2410|GAU|8|16
84|27.5860|91.8580|GAU|13|24
85|27.2640|92.4190|GAU|7|12
86|28.5990|94.1250|DIB|15|24
87|27.5930|93.8390|HGI|5|24
88|28.0660|95.3260|DIB|5|16
89|28.7890|95.9020|DIB|13|24
90|27.4920|96.3860|DIB|6|32
91|27.0740|92.6520|GAU|6|24
92|27.6710|95.8650|DIB|4|16
93|27.3389|88.6065|IXB|4.5|16
94|27.3000|88.2350|IXB|5|16
95|27.3710|88.2220|IXB|6|16
96|27.3070|88.3640|IXB|4.5|12
97|27.5180|88.5250|IXB|6|16
98|27.6890|88.7430|IXB|9|24
99|27.3750|88.7620|IXB|6|8
100|27.0410|88.2660|IXB|3|16
101|27.1050|88.0020|IXB|5|32
102|25.6750|94.1086|DMU|3|24
103|23.7270|92.7170|AJL|1.5|16
104|23.8310|91.2860|IXA|1|16
105|27.7172|85.3240|KTM|.5|24
106|27.7170|85.5200|KTM|2|8
107|28.2096|83.9856|PKR|.5|24
108|28.4010|83.7190|PKR|3|40
109|28.0000|85.4300|KTM|8|48
110|27.5670|84.4970|BHR|1|24
111|27.9380|84.4060|KTM|5|12
112|19.5490|73.6910|BOM|5|16
113|19.3890|73.7760|BOM|4.5|12
114|18.7550|73.4100|PNQ|2|12
115|20.0059|73.7900|ISK|.5|12
116|20.0260|75.1780|IXU|1|16
117|17.9300|73.6470|PNQ|3|16
118|16.0470|73.4620|GOX|2|24
119|16.9900|73.3120|GOX|6|16
120|15.2993|74.1240|GOX|1|24
121|21.1240|70.8240|RAJ|4|24
122|20.8880|70.4020|RAJ|4|12
123|22.4707|70.0577|JGA|.5|16
124|20.5790|73.7470|STV|4|16
125|22.4670|78.4340|BHO|4.5|32
126|23.1300|79.8010|JLR|1|8
127|25.3510|78.6410|JHS|.5|16
128|24.8318|79.9199|HJR|.5|24
129|22.3340|80.6110|JLR|4|24
130|22.1770|75.5840|IDR|2.5|16
131|15.3350|76.4600|HBX|3.5|24
132|14.5479|74.3188|GOX|4|24
133|15.2470|74.6290|HBX|2|16
134|13.3170|75.7730|IXE|4|24
135|10.0890|77.0590|COK|4|24
136|9.4981|76.3388|COK|1.5|16
137|11.9230|93.0020|IXZ|3|32
'''
rows={int(r.split('|')[0]):r.split('|')[1:] for r in raw.strip().splitlines()}
S={
'air':('IndiGo route directory','https://www.goindigo.in/domestic-flights.html'),
'rail':('Indian Railways fare enquiry','https://indianrail.gov.in/enquiry/FARE/FareEnquiry.html'),
'irctc':('IRCTC reservation','https://www.irctc.co.in/nget/train-search'),
'road':('HRTC route / reservation portal','https://online.hrtchp.com/'),
'hp':('Himachal Tourism','https://himachaltourism.gov.in/'),
'uk':('Uttarakhand Tourism','https://uttarakhandtourism.gov.in/'),
'jk':('Jammu & Kashmir Tourism','https://tourism.jk.gov.in/'),
'ladakh':('Ladakh Tourism advisory','https://tourism.ladakh.gov.in/advisory'),
'lehpermit':('Leh foreign / overseas permit portal','https://www.lahdclehpermit.in/register-as-overseas'),
'arunachal':('Arunachal foreign PAP instructions','https://arunachaltourism.com/protected-area-permit/'),
'sikkim':('Sikkim RAP entry permission','https://www.sikkimtourism.gov.in/rap'),
'sikkimpap':('Sikkim protected-area permits / restrictions','https://www.sikkimtourism.gov.in/pap'),
'nepermit':('Ministry of Home Affairs PAP/RAP guidance','https://www.mha.gov.in/en/divisionofmha/foreigners-division/protected-area-permit-pap-restricted-area-permit-rap'),
'meg':('Meghalaya Tourism activities & local contacts','https://www.meghalayatourism.in/'),
'assam':('Assam Tourism destinations','https://assamtourism.gov.in/Explore.php'),
'nagaland':('Nagaland Tourism','https://tourism.nagaland.gov.in/'),
'nepal':('Nepal Tourism Board','https://ntb.gov.np/'),
'tims':('Nepal route-specific guide / TIMS rules','https://ntb.gov.np/plan-your-trip/before-you-come/tims-card'),
'mh':('Maharashtra Tourism','https://maharashtratourism.gov.in/'),
'gujarat':('Gujarat Tourism','https://gujarattourism.com/'),
'mp':('Madhya Pradesh Tourism','https://www.mptourism.com/'),
'kar':('Karnataka Tourism','https://karnatakatourism.org/'),
'kerala':('Kerala Tourism','https://www.keralatourism.org/'),
'andaman':('Andaman Tourism information','https://www.andamantourism.gov.in/'),
'imd':('India Meteorological Department climate services','https://mausam.imd.gov.in/responsive/climate_services.php'),
'shillongwx':('IMD Shillong monthly normals (1981–2010)','https://city.imd.gov.in/citywx/extreme/DEC/shillong2.htm'),
'lehwx':('IMD Leh monthly normals (1951–1980; historic baseline)','https://city.imd.gov.in/citywx/extreme/JAN/leh2.htm'),
'ktmwx':('WMO Kathmandu monthly climate','https://worldweather.wmo.int/en/city.html?cityId=114'),
'flightdelktm':('Air India DEL–KTM route / fare anchor','https://www.airindia.com/en-in/book-flights/delhi-to-kathmandu-flights'),
'flightdelixb':('Air India DEL–IXB route / fare anchor','https://www.airindia.com/en-in/book-flights/delhi-to-bagdogra-flights'),
'flightdelsxr':('Air India DEL–SXR route / fare anchor','https://www.airindia.com/en-in/book-flights/delhi-to-srinagar-flights'),
'flightdelixl':('Air India DEL–IXL route / fare anchor','https://www.airindia.com/en-in/book-flights/delhi-to-leh-flights'),
'flightdelgau':('Air India DEL–GAU route / fare anchor','https://www.airindia.com/en-in/book-flights/delhi-to-guwahati-flights'),
'flightdelded':('Air India DEL–DED fare anchor','https://www.airindia.com/en/book-flights/delhi-to-dehradun-flights'),
'flightdeldhm':('IndiGo Dharamshala routes','https://aem-skyplus-prod-canary.goindigo.in/domestic-flights/flights-to-dharamshala.html'),
'railvns':('22436 timetable / fare listing','https://erail.in/train-fare/22436'),
'railcdg':('Delhi–Chandigarh timetable / historical fare structure','https://www.pib.gov.in/PressReleasePage.aspx?PRID=1867466&lang=2&reg=48'),
'raildib':('Guwahati–Dibrugarh rail ranges','https://erail.in/trains-between-stations/guwahati-GHY/dibrugarh-DBRG'),
'buddha':('Buddha Air published flight durations','https://www.buddhaair.com/detail/flight-information'),
'buddhapkr':('Buddha Air Kathmandu–Pokhara route','https://www.buddhaair.com/flight-routes/flights-from-kathmandu-to-pokhara'),
'incredible':('Incredible India destination information','https://www.incredibleindia.gov.in/'),
'uttbooking':('Uttarakhand pilgrimage registration','https://registrationandtouristcare.uk.gov.in/'),
'gir':('Official Gir safari reservation','https://girlion.gujarat.gov.in/'),
'mpbooking':('MP forest safari reservation','https://forest.mponline.gov.in/'),
'caving':('Meghalaya Tourism caving operator directory','https://rc-www.meghalayatourism.in/plan-your-trip-5/tour-operators-packages/'),
'rafting':('Aquaterra river trips / Rishikesh operator lead','https://aquaterra.in/river-rafting-in-india/'),
'dayara':('Indiahikes Dayara trek / operator itinerary','https://indiahikes.com/dayara-bugyal-trek'),
'kedarkantha':('Indiahikes Kedarkantha trek / operator itinerary','https://www.indiahikes.com/kedarkantha-trek'),
}
hubraw='''DEL|Delhi · DEL / NDLS|28.614|77.209
IXC|Chandigarh · IXC / CDG|30.733|76.779
MAN|Manali bus / road gateway|32.243|77.189
DHM|Dharamshala · DHM|32.165|76.263
SXR|Srinagar · SXR|33.987|74.774
IXJ|Jammu · IXJ / JAT|32.69|74.837
IXL|Leh · IXL|34.136|77.546
DED|Dehradun · DED / Haridwar HW|30.19|78.18
KGM|Kathgodam railhead · KGM|29.267|79.548
ATQ|Amritsar · ATQ / ASR|31.71|74.798
VNS|Varanasi · VNS / BSB|25.453|82.859
AGR|Agra rail gateway · AGC|27.157|77.989
LKO|Lucknow · LKO / LKO rail|26.761|80.884
SHL|Shillong road gateway|25.579|91.893
GAU|Guwahati · GAU / GHY|26.106|91.586
JRH|Jorhat · JRH|26.731|94.176
DIB|Dibrugarh · DIB / DBRG|27.483|95.017
LMG|Lumding railhead · LMG|25.752|93.17
HGI|Itanagar · HGI / Naharlagun NHLN|27.0|93.65
IXB|Bagdogra · IXB / New Jalpaiguri NJP|26.682|88.328
DMU|Dimapur · DMU / DMV|25.884|93.772
AJL|Aizawl · AJL|23.84|92.62
IXA|Agartala · IXA / AGTL|23.887|91.24
KTM|Kathmandu · KTM|27.697|85.359
PKR|Pokhara · PKR|28.184|83.982
BHR|Bharatpur / Chitwan · BHR|27.679|84.429
BOM|Mumbai · BOM / Mumbai rail|19.09|72.866
PNQ|Pune · PNQ / PUNE|18.582|73.919
ISK|Nashik road / NK rail gateway|20.0|73.8
IXU|Chhatrapati Sambhajinagar · IXU|19.862|75.398
GOX|North Goa · GOX / Madgaon MAO|15.744|73.86
RAJ|Rajkot · HSR / Rajkot rail|22.38|71.86
JGA|Jamnagar · JGA|22.465|70.013
STV|Surat · STV / ST|21.114|72.742
BHO|Bhopal · BHO / BPL|23.287|77.337
JLR|Jabalpur · JLR / JBP|23.177|80.052
JHS|Jhansi · VGLJ rail|25.44|78.565
HJR|Khajuraho · HJR / KURJ|24.818|79.918
IDR|Indore · IDR / INDB|22.722|75.801
HBX|Hubballi · HBX / UBL|15.361|75.084
IXE|Mangaluru · IXE / MAJN|12.962|74.89
COK|Kochi · COK / ERS|10.152|76.401
IXZ|Sri Vijaya Puram · IXZ|11.641|92.729
CCU|Kolkata · CCU / HWH|22.654|88.447
BLR|Bengaluru · BLR / SBC|13.199|77.707
MAA|Chennai · MAA / MAS|12.994|80.17
AMD|Ahmedabad · AMD / ADI|23.073|72.634'''
hubs={}
for line in hubraw.splitlines():
 c,n,lat,lon=line.split('|');hubs[c]={'id':c,'name':n,'lat':float(lat),'lon':float(lon),'hub':True}
regions=[(20,'Himachal','hp'),(27,'Kashmir & Jammu','jk'),(35,'Ladakh','ladakh'),(51,'Uttarakhand','uk'),(59,'North India cities','incredible'),(72,'Meghalaya','meg'),(82,'Assam','assam'),(92,'Arunachal','arunachal'),(101,'Sikkim & Bengal hills','sikkim'),(104,'Other Northeast','nagaland'),(111,'Nepal','nepal'),(120,'Maharashtra & Goa','mh'),(124,'Gujarat','gujarat'),(130,'Central India','mp'),(137,'South & islands','kar')]
def clean(s):return re.sub(r'\s*\[[A-Z][^\]]*\]','',s).replace('**','').strip()
def profile(i):
 if 28<=i<=35 or i==18:return 'leh'
 if i in [4,17,19,26,40,41,42,43,44,45,46,47,51,84,86,89,98,101,108,109]:return 'highhill'
 if i<=20 or 21<=i<=25 or i in [27,48,49,83,85,87,93,94,95,96,97,99,100,102,103]:return 'hill'
 if 60<=i<=68 or i in [71,72]:return 'shillong'
 if i in [105,106]:return 'kathmandu'
 if i==137:return 'island'
 if 118<=i<=120 or i in [122,123,132,136]:return 'coast'
 if i in [112,113,114,115,116,117,124,125,131,133,134,135]:return 'ghats'
 if 69<=i<=92 or i in [104,107,110,111]:return 'northeast'
 return 'plains'
permits={
'general':{'level':'standard','label':'Standard entry','text':'No special state-entry permit identified for this representative town. Forests, safaris, monuments and individual trails can require their own tickets or permissions.','links':[]},
'ladakh':{'level':'permit','label':'Protected-area review','text':'Foreign visitors: protected areas need approved permission and route eligibility. Confirm the current foreign-tourist circuit; Hanle, frontier roads and restricted extensions are not assumed accessible. Rest at least 48 hours after arrival in Leh before going higher.','links':['lehpermit','nepermit','ladakh']},
'arunachal':{'level':'permit','label':'Foreign PAP required','text':'Foreign tourists use a Protected Area Permit, usually through an approved local tour operator, not the domestic ILP. Obtain approval for the exact circuit. Bum La and other frontier areas are not assumed eligible. Special travel documents do not automatically remove restrictions.','links':['arunachal','nepermit']},
'sikkim':{'level':'permit','label':'RAP / route-specific PAP','text':'Foreign-passport visitors need state-entry RAP and, for protected circuits, PAP through approved arrangements. Nathula and Gurudongmar are listed as unavailable to foreigners; specified northern valleys and Tsomgo are conditional. Confirm eligibility for your document type and group/guide rules.','links':['sikkim','sikkimpap','nepermit']},
'hp':{'level':'check','label':'Route permit check','text':'Some Kinnaur / Spiti routes pass protected areas. Foreign visitors must confirm the exact route and obtain permission where required; do not apply Indian-citizen advice automatically.','links':['hp','nepermit']},
'frontier':{'level':'check','label':'Eligibility unresolved','text':'Frontier access and foreign-visitor eligibility are unresolved. Obtain written route-specific confirmation before relying on this destination; inclusion on this map is not authorization.','links':['nepermit']},
'ne':{'level':'permit','label':'Foreign entry review','text':'Protected-area rules in the Northeast have changed. Confirm current foreign-passport PAP requirements and approved circuits with the authorities or a registered operator before booking.','links':['nepermit','nagaland']},
'treknepal':{'level':'check','label':'Trekking permits / guide','text':'Nepal has separate entry rules. Route-specific conservation permits, licensed-guide and TIMS requirements may apply; check the actual trek rather than assuming independent access.','links':['tims','nepal']},
'pilgrimage':{'level':'check','label':'Season + registration','text':'The main Himalayan shrine normally closes for winter. Register when pilgrimage is operating; winter worship takes place at lower-altitude seats. Main shrine and winter seat are different destinations.','links':['uttbooking','uk']},
'forest':{'level':'check','label':'Protected-site booking','text':'Arrange the exact safari, park entry or guided trail permission. Access to one zone does not grant entry to all zones; wildlife sightings are not guaranteed.','links':[]},
}
dests=[]
for m in re.finditer(r'^### (\d{3})\. (.*?)\n(.*?)(?=\n### |\n## |\Z)',bank,re.M|re.S):
 i=int(m[1])
 if i>137:continue
 head=m[2];name=head.split(' — ')[0];meta=head.split(' — ',1)[1] if ' — ' in head else ''
 lat,lon,hub,access,visit=rows[i];region,source=next((r,s) for end,r,s in regions if i<=end)
 desc=clean(m[3]);text=(name+' '+desc).lower();tags=[]
 for t,pat in [('Hikes','trek|hik|trail|walk|ridge|peak'),('Mountains','mountain|himal|snow|valley|alpine'),('Water','river|lake|boat|raft|kayak|waterfall|sea|coast'),('Caves','cave|caving|canyon'),('Wildlife','wildlife|bird|safari|forest|rhino'),('Culture','temple|monaster|sacred|food|village|architecture'),('Flight sports','paraglid|bungee'),('Night skies','astro|night sk|dark.sk|night photo')]:
  if re.search(pat,text):tags.append(t)
 p='general'
 if 28<=i<=35:p='ladakh'
 if 83<=i<=92:p='arunachal'
 if 93<=i<=99:p='sikkim'
 if i in [17,18]:p='hp'
 if i in [26]:p='frontier'
 if i in [102,103]:p='ne'
 if i in [108,109]:p='treknepal'
 if i in [41,42,51]:p='pilgrimage'
 if i in [35,50,70,73,74,78,79,80,90,91,110,121,125,129]:p='forest' if p=='general' else p
 closed=[11,12,1,2,3,4] if i in [26,41,42] else [11,12,1,2,3,4,5] if i==51 else []
 caution=bool(re.search('conditional|later-season|demanding|specialist',meta))
 # Short activity list comes from the bank's first descriptive clauses; retain full bank copy too.
 first=desc.split('. ')[0].replace('Points of interest: ','')
 acts=[x.strip().capitalize() for x in first.split(';')][:6]
 if len(acts)<2:acts=[first, 'See the destination notes for seasonal options and individual sights.']
 days=max(.5,round(float(visit)/8*2)/2)
 links=[]
 if 60<=i<=72:links+=['meg']
 if i in [41,42,51]:links+=['uttbooking']
 if i in [108,109]:links+=['tims']
 if i==121:links+=['gir']
 if i in [125,128,129]:links+=['mpbooking']
 if i in [135,136]:links=['kerala']
 if i==137:links=['andaman']
 dests.append(dict(id=str(i).zfill(3),num=i,name=name,lat=float(lat),lon=float(lon),hub=hub,access=float(access),visitHours=float(visit),days=days,region=region,source=source,description=desc,activities=acts,tags=tags,fit='A' if meta.startswith('A') else 'B',climate=profile(i),permit=p,closedMonths=closed,decCaution=caution,seasonNote=clean(meta),links=list(dict.fromkeys(links)),country='Nepal' if 105<=i<=111 else 'India'))
assert len(dests)==137
nodes=list(hubs.values())+[dict(id=d['id'],name=d['name'],lat=d['lat'],lon=d['lon'],hub=False) for d in dests]
edges=[]
def edge(a,b,mode,hours,lo,hi,source='air',note='',basis='person',months=None,evidence='Planning allowance',access=False):
 assert a in hubs or a in [d['id'] for d in dests],a
 assert b in hubs or b in [d['id'] for d in dests],b
 edges.append(dict(id='e'+str(len(edges)),a=a,b=b,mode=mode,hours=hours,low=lo,high=hi,source=source,note=note,basis=basis,months=months or list(range(1,13)),evidence=evidence,access=access))
# Explicit major-airport corridors. Values are one-way economy planning bands, not date-specific quotes.
flightrows='''DEL SXR 1.35 5000 11000 flightdelsxr
DEL IXL 1.25 5500 12000 flightdelixl
DEL DHM 1.5 5000 12000 flightdeldhm
DEL IXC 1 3000 6500 air
DEL ATQ 1.25 4500 10000 air
DEL IXJ 1.4 4500 9000 air
DEL DED 1 4000 7000 flightdelded
DEL VNS 1.5 4500 9000 air
DEL LKO 1.2 3500 7000 air
DEL GAU 2.5 6500 12000 flightdelgau
DEL IXB 2 6000 11000 flightdelixb
DEL KTM 1.6 8000 15000 flightdelktm
DEL BOM 2.3 5000 10000 air
DEL PNQ 2.2 5000 10000 air
DEL AMD 1.7 4000 8500 air
DEL BHO 1.4 4000 8500 air
DEL IDR 1.6 4500 9000 air
DEL JLR 1.6 5000 10000 air
DEL BLR 2.8 6000 12000 air
DEL MAA 2.8 6000 12000 air
DEL CCU 2.3 5000 10000 air
DEL GOX 2.6 6500 13000 air
DEL HGI 2.8 7000 14000 air
DEL DIB 2.8 7000 14000 air
DEL DMU 2.8 7000 14000 air
GAU CCU 1.2 3500 7500 air
GAU IXB 1.1 3000 6500 air
GAU DIB 1.1 3000 7000 air
GAU JRH 1 3500 8000 air
GAU DMU 1 3000 7000 air
GAU IXA 1 3000 7000 air
GAU AJL 1.1 3500 8000 air
GAU BOM 3.2 7000 14000 air
GAU BLR 3.1 7000 14000 air
GAU IXC 3 6500 13000 air
CCU IXB 1.2 3500 7500 air
CCU AJL 1.3 4000 8500 air
CCU IXA 1 3500 7500 air
CCU KTM 1.5 9000 18000 buddha
VNS KTM .85 9000 18000 buddha
KTM PKR .45 11000 16000 buddhapkr
KTM BHR .42 8500 13000 buddha
BOM PNQ .9 3000 6000 air
BOM CCU 2.7 5500 11000 air
BOM GOX 1.2 3500 8000 air
BOM AMD 1.2 3000 6500 air
BOM RAJ 1.25 4000 8500 air
BOM JGA 1.4 4500 9500 air
BOM IXU 1 3500 7500 air
BOM BLR 1.8 4000 9000 air
BOM MAA 2 4500 9500 air
BOM COK 2 4500 10000 air
BOM IXE 1.6 4000 9000 air
BOM IXZ 3.5 8500 17000 air
BLR HBX 1.3 3500 8000 air
BLR IXE 1 3000 7000 air
BLR COK 1.1 3000 7000 air
BLR GOX 1.3 3500 8000 air
BLR MAA 1 3000 6500 air
BLR CCU 2.7 5500 11000 air
MAA IXZ 2.3 6000 13000 air
CCU IXZ 2.3 6500 14000 air'''
for line in flightrows.splitlines():
 a,b,h,lo,hi,src=line.split();ev='Published route/time anchor; budget range estimated' if src!='air' else 'Route-network lead; time & fare allowance'
 edge(a,b,'flight',float(h),int(lo),int(hi),src,'Economy. Recheck dates and nonstop availability; reverse direction uses the same planning band. Nepal domestic fares budgeted for a foreign passport, converted to INR.',evidence=ev)
# Rail corridors are explicitly listed; class is an allowance, not an asserted live train departure.
railrows='''DEL IXC 3 700 1200 railcdg
DEL ATQ 6 900 1700 rail
DEL IXJ 9 1000 1800 rail
DEL VNS 8 1800 2300 railvns
DEL LKO 6.5 1000 1700 rail
DEL AGR 2 600 1400 rail
DEL KGM 6 650 1500 rail
DEL DED 5 700 1500 rail
DEL JHS 4.8 900 1700 rail
DEL BHO 8.5 1200 2200 rail
DEL BOM 16 1800 3200 rail
DEL CCU 18 2000 3800 rail
DEL GAU 28 2300 4500 rail
DEL AMD 13 1400 2600 rail
IXC ATQ 4.5 500 1100 rail
IXC DED 5 500 1200 rail
ATQ IXJ 4.5 500 1200 rail
AGR LKO 5.5 600 1300 rail
AGR JHS 3 500 1200 rail
LKO VNS 5.5 500 1300 rail
VNS CCU 12 1100 2400 rail
JHS BHO 4 500 1300 rail
JHS HJR 5.5 450 1200 rail
BHO JLR 5 600 1400 rail
BHO IDR 5.5 600 1400 rail
BHO BOM 12 1200 2500 rail
GAU IXB 7.5 600 1500 rail
GAU LMG 3.5 350 900 rail
GAU DIB 10.5 700 1700 raildib
GAU DMU 5.5 450 1200 rail
GAU HGI 8 650 1500 rail
CCU IXB 9 900 1800 rail
BOM PNQ 3.5 400 1100 rail
BOM ISK 3.5 400 1100 rail
BOM STV 3.5 500 1200 rail
BOM AMD 6 800 1800 rail
BOM GOX 10 900 2000 rail
BOM IXE 16 1300 2800 rail
PNQ HBX 10 1000 2200 rail
GOX HBX 5 500 1300 rail
GOX IXE 5.5 600 1400 rail
IXE COK 10 900 1900 rail
AMD RAJ 4.5 500 1200 rail
RAJ JGA 2 300 800 rail
BLR HBX 8 700 1700 rail
BLR MAA 5 650 1500 rail
BLR COK 11 1000 2300 rail'''
for line in railrows.splitlines():
 a,b,h,lo,hi,src=line.split();edge(a,b,'train',float(h),int(lo),int(hi),src,'AC chair car / 3A planning band. Uses a representative railhead, not necessarily the airport location. Terminal changes and actual running days must be checked.',evidence='Timetable anchor + estimated fare band' if src!='rail' else 'Corridor / class budget allowance')
roadrows='''DEL MAN 14 1400 2200
DEL DHM 11 1200 2000
IXC MAN 8 800 1500
IXC DHM 6 600 1300
DHM MAN 7 700 1500
DEL IXC 5 500 1000
DEL DED 6 500 1100
IXJ SXR 8 700 1500
GAU SHL 3 300 800
GAU JRH 7 600 1400
JRH DIB 4 400 1000
GAU HGI 8 700 1500
LMG DMU 2 250 600
KTM PKR 9 1000 2200
KTM BHR 7 900 1800
PKR BHR 6 800 1700
PNQ ISK 5 500 1100
ISK IXU 4 500 1100
AMD RAJ 4 500 1100
STV AMD 5 500 1200
IDR BHO 4.5 500 1100
JLR HJR 5 600 1400
GOX HBX 4 450 1100'''
for line in roadrows.splitlines():
 a,b,h,lo,hi=line.split();edge(a,b,'road',float(h),int(lo),int(hi),'road' if a in ['DEL','IXC','DHM'] else 'incredible','Intercity bus/shared-road budget allowance, not a confirmed scheduled departure. Overnight accommodation excluded.')
edge('MAN','IXL','road',14,2500,5000,'ladakh','Seasonal Manali–Leh corridor; NOT a winter option.',months=[6,7,8,9],evidence='Seasonal corridor; editorial allowance')
edge('SXR','IXL','road',12,2200,4500,'ladakh','Seasonal Srinagar–Leh corridor; verify opening.',months=[5,6,7,8,9,10],evidence='Seasonal corridor; editorial allowance')
# Regional access: town gateway -> destination, not hotel pickup, sightseeing or attraction admission.
for d in dests:
 a=d['access']
 private=d['num'] in list(range(28,36))+list(range(83,93))+[26,62,69,70,98,101]
 if a==0:lo=hi=0
 elif private:lo=int(max(1200,a*450)/100)*100;hi=int(max(2000,a*750)/100)*100
 else:lo=int(max(100,a*120)/50)*50;hi=int(max(250,a*280)/50)*50
 edge(d['id'],d['hub'],'road',a,lo,hi,d['source'],'Regional gateway approach. '+('Private vehicle allowance split across up to 4 travelers per vehicle.' if private else 'Public/shared-road budget allowance; exact service and last-mile availability unverified.')+' Hotel transfers, sightseeing and entry/activity fees excluded.',basis='vehicle' if private else 'person',access=True,months=[5,6,7,8,9,10] if d['num']==26 else None)
# Explicit local cross-links prevent nearby stops being forced back through an airport gateway.
localrows='''001 002 .75
001 003 2
001 013 2
001 019 4
002 005 2.5
005 006 1
005 007 1.5
006 007 2
008 009 2
008 010 2
008 011 1
010 011 1
010 020 5
014 015 1.5
014 016 2
016 017 6
017 018 9
021 022 2
021 023 2.5
021 024 3
021 025 2
021 026 7
028 033 4
028 029 5
028 030 6
028 031 7
028 032 8
029 030 6
030 032 5
031 032 4
036 037 1
036 038 1
036 039 2
039 040 4
040 041 3
040 043 5
043 042 2
043 051 2
047 048 5
048 049 3
049 050 2
052 053 3
054 055 1
056 058 1.5
060 061 .5
060 063 .75
060 064 .5
064 067 2
063 065 3
065 066 1.5
065 068 2
066 067 1
068 062 3
071 060 2.5
071 068 2.5
071 072 3
069 070 3
073 075 3.5
073 082 4
075 076 4.5
076 079 2
076 080 2
076 082 2.5
077 078 2
083 084 5
083 085 1.5
085 091 4
086 088 10
087 088 9
088 089 9
088 092 4
090 092 3
093 094 5
093 096 3
093 097 4
093 098 6
093 099 2
094 095 2
094 096 2.5
100 101 2
100 093 4
105 106 2
105 111 5
107 108 3
107 111 4
107 110 6
112 113 2
112 115 2.5
113 114 4
114 117 3.5
118 119 4
118 120 3
121 122 1.5
125 130 7
126 129 4
127 128 4
131 133 4.5
132 133 3
132 134 6
135 136 5'''
for line in localrows.splitlines():
 a,b,h=line.split();h=float(h)
 if a=='017' and b=='018':months=list(range(5,11))
 elif a=='021' and b=='026':months=list(range(5,11))
 else:months=None
 edge(a,b,'road',h,round(max(200,h*160)/50)*50,round(max(500,h*360)/50)*50,'incredible','Explicit regional corridor; planning time and shared/public-road budget allowance. No last-mile sightseeing or guaranteed service.',months=months,evidence='Editorial regional allowance')
# Historical station normals are kept separate from intentionally coarse regional planning bands.
climates={
'shillong':{'name':'Shillong station normals','source':'shillongwx','exact':True,'low':[5.9,7.5,11.1,13.8,15.5,17.4,17.9,17.7,16.7,14.3,10.5,7.2],'high':[14.9,17,21,23.2,23.4,24,23.9,24.1,23.3,21.8,19.1,16],'rain':[14,19,46,129,267,429,497,311,277,212,39,13]},
'leh':{'name':'Historic Leh station baseline; outlying plateaus colder','source':'lehwx','exact':True,'low':[-14,-11,-6,-1,3,7,11,10,6,-1,-7,-12],'high':[-2,2,7,12,16,22,25,25,22,15,8,2],'rain':[10,8,11,9,9,4,15,15,9,8,4,5]},
'kathmandu':{'name':'Kathmandu station climate','source':'ktmwx','exact':True,'low':[2,4,8,11,16,19,20,20,18,13,7,3],'high':[18,20,24,27,28,28,28,28,27,26,23,19],'rain':[14,17,31,54,114,256,360,314,183,59,8,14]},
'hill':{'name':'Mid-elevation hill planning band','source':'imd','low':[0,2,6,10,14,17,18,18,15,10,5,1],'high':[11,13,17,22,25,27,26,25,24,21,17,12]},
'highhill':{'name':'High-mountain planning band; exposure varies greatly','source':'imd','low':[-8,-7,-3,1,5,8,10,9,6,1,-3,-7],'high':[3,5,9,13,17,20,20,20,18,13,8,4]},
'plains':{'name':'North/central plains planning band','source':'imd','low':[8,11,16,22,26,28,27,26,24,19,13,9],'high':[21,25,31,36,39,38,34,33,34,33,28,23]},
'northeast':{'name':'Northeast low-valley / lower-hill planning band','source':'imd','low':[10,13,17,21,23,25,25,25,24,21,16,11],'high':[23,25,29,30,31,32,32,33,32,30,27,24]},
'coast':{'name':'West-coast planning band','source':'imd','low':[20,21,23,25,26,25,24,24,24,24,23,21],'high':[30,31,32,33,33,30,29,29,30,31,32,31]},
'ghats':{'name':'Western Ghats plateau planning band','source':'imd','low':[12,14,17,20,22,21,20,20,19,17,14,12],'high':[27,29,32,33,32,27,25,25,27,28,28,27]},
'island':{'name':'Tropical-island planning band','source':'imd','low':[23,23,24,25,25,24,24,24,24,24,24,23],'high':[29,30,31,32,31,29,29,29,29,29,29,29]},
}
data=dict(researched='2026-10-18',title='India Trip Generator',destinations=dests,nodes=nodes,edges=edges,sources={k:{'label':v[0],'url':v[1]} for k,v in S.items()},permits=permits,climates=climates)
from expansion import augment
data=augment(data)
from expansion_v3 import augment as augment_v3
data=augment_v3(data)
from media_data import augment as augment_media
data=augment_media(data)
from expansion_v5 import augment as augment_v5
data=augment_v5(data)
output=Path(os.environ.get('TRIP_DATA_OUTPUT',str(ROOT/'dist'/'data.json')))
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print(f"{len(data['destinations'])} destinations · {len(data['nodes'])} nodes · {len(data['edges'])} explicit bidirectional corridors")
