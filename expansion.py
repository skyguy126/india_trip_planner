"""Nationwide v2 additions. Stable IDs continue the original saved-plan catalog."""
import re

# id|name|latitude|longitude|gateway|access hours|visit hours|region|climate|activities|notes
RAW='''138|Jaipur|26.9124|75.7873|JAI|.5|20|Rajasthan|desert|Amber Fort; Nahargarh sunset; Hawa Mahal streets; stepwells and old-city food|Restored as a revisit option because you explicitly reopened Rajasthan. Combine architecture, hilltop views and street photography; do not expect a museum-heavy stay. Winter is pleasant, while summer sightseeing needs heat-aware timing.
139|Udaipur|24.5854|73.7125|UDR|.75|20|Rajasthan|desert|Lake Pichola boat outing; City Palace exterior and courtyards; Bahubali Hills; Sajjangarh viewpoints|Restored as a revisit option. Lakes, Aravalli scenery and evening photography are the main draw. Boat operations and hill access vary; nearby rural stays can offer a different experience from a repeat city checklist.
140|Chittorgarh|24.8887|74.6269|UDR|2.5|8|Rajasthan|desert|Fort plateau; Vijay Stambh; Rana Kumbha Palace; hilltop sunset views|A previously visited place now deliberately retained for a possible revisit. Explore the large fort landscape and chosen architectural sites rather than assuming every monument fits a short stop. The film association in the original notes is a personal reference, not a newly verified scene-location claim.
141|Jodhpur and Osian|26.2389|73.0243|JDH|.5|20|Rajasthan|desert|Mehrangarh Fort; blue-city lanes; Toorji stepwell; Osian temples and dune-country outing|Strong architectural and landscape photography. Osian adds a smaller desert-country excursion without requiring the full Jaisalmer dune stay. Ask an operator which activity is actually included; animal rides are optional, not the point of the visit.
142|Jaisalmer|26.9157|70.9083|JSA|.75|20|Rajasthan|desert|Living fort lanes; Patwon havelis; Gadisar Lake; Kuldhara village ruins|A high-interest desert addition now that the exclusion is lifted. The fort is also a living neighborhood, so use responsible photography and lodging choices. Winter light is excellent for stone and landscape images; flight services can be seasonal.
143|Khuri and Sam dune country|26.8260|70.5360|JSA|1.5|16|Rajasthan|desert|Dune sunset; guided desert walks; village stay; night-sky photography|Research quieter Khuri-area camps alongside busier Sam. Check music/noise, light pollution and the actual dune setting before choosing a camp. Dark skies depend on the moon and camp lighting. Desert vehicle activities require an appropriate permitted operator and are not a guarantee of unrestricted off-roading.
144|Bikaner and Deshnok|28.0229|73.3119|BKB|.5|12|Rajasthan|desert|Junagarh Fort; old-city havelis; Rampuria streets; Karni Mata temple at Deshnok|A less obvious heritage-city alternative with strong architectural details and local food. The Deshnok temple has a distinctive devotional setting; choose it for genuine cultural interest and follow local rules. Heat is substantial outside the winter window.
145|Pushkar and Ajmer|26.4897|74.5511|JAI|3|12|Rajasthan|desert|Pushkar lake ghats; Brahma temple; Savitri hill viewpoint; Ajmer Sharif atmosphere|Temples, sacred streets and ridge views offer a cultural break between outdoor regions. The camel fair is a date-specific event, not an all-winter feature. Respect photography and food rules around sacred places; fair crowds transform the experience.
146|Bundi|25.4305|75.6499|JAI|4|12|Rajasthan|desert|Garh Palace; Taragarh viewpoints; Raniji stepwell; old-town lanes|Strong fit for wandering and photography in a compact heritage town. Palace rooms, paintings and upper fort areas can have separate access or conservation limits. Good alternative to repeating only the most famous Rajasthan cities.
147|Ranthambore|26.0173|76.5026|JAI|3.5|24|Rajasthan|desert|Authorized tiger-reserve safari; Ranthambore Fort; lake landscapes; birding|Plan legal safari zones and multiple outings if wildlife is central. Tigers are not guaranteed. Core safari access is seasonal and zone-specific; a fort visit is a separate activity from a wildlife permit. Winter is comfortable, while summer often changes visibility and heat exposure.
148|Bharatpur and Deeg|27.2152|77.4895|AGR|1.25|12|Rajasthan|plains|Keoladeo birding; cycle or cycle-rickshaw wildlife visit; Deeg palace gardens; wetland photography|Excellent for active bird photography and a gentler outdoor day. Migratory bird numbers depend on winter conditions and water management. Keoladeo has protected-site admission and vehicle rules; use a knowledgeable local naturalist if birds are the main goal.
149|Sariska and Alwar|27.3280|76.4330|JAI|2.5|16|Rajasthan|desert|Authorized Sariska safari; Alwar architecture; Siliserh Lake; Bhangarh ruins during legal hours|Combines forest, hills and heritage. Do not build expectations around guaranteed tigers or after-hours access to ruins. Safaris and local monument visits have different entry arrangements. Stronger if you want a varied landscape segment than only a city stay.
150|Kumbhalgarh and Ranakpur|25.1470|73.5830|UDR|2.5|12|Rajasthan|desert|Kumbhalgarh Fort walls; Aravalli viewpoints; Ranakpur Jain temple; village landscapes|A strong outdoor architecture extension to Udaipur. Temple visiting periods and photography rules differ from fort access. Sanctuary outings need authorization; simply being near the forest does not permit independent wildlife trekking.
151|Mount Abu|24.5926|72.7156|AMD|4.5|16|Rajasthan|hill|Dilwara temples; Guru Shikhar; Nakki Lake; authorized forest walks|Rajasthan's hill alternative combines sacred architecture and viewpoints. Winter nights can be cold despite the state's desert reputation. Follow temple camera rules and verify legal access to sanctuary trails rather than assuming every mapped path is public.
152|Shekhawati havelis|27.9800|75.1400|JAI|3|16|Rajasthan|desert|Mandawa streets; Nawalgarh havelis; fresco details; village food|Architectural photography and slower town exploration, with individual havelis often privately owned or operated. Arrange access and fees locally. Best if you enjoy looking closely at painted facades and inhabited streets rather than a long museum circuit.
153|Kota and Chambal landscapes|25.2138|75.8648|JAI|4|12|Rajasthan|desert|Chambal river viewpoints; Garadia Mahadev; Kishore Sagar; Seven Wonders Park|Kota restores a geographically relevant Badrinath Ki Dulhania filming lead from the earlier corrections. River cliffs offer more outdoor appeal than a pure film checklist. Confirm viewpoint access and boating; water release and entry conditions can change.
154|Jawai and rural Pali|25.1160|73.1430|JDH|3.5|24|Rajasthan|desert|Naturalist-led leopard outings; granite hills; reservoir birds; invited village visits|Excellent wildlife-plus-landscape photography. Choose a responsible local operator and confirm the legal viewing area. Leopards are wild and sightings uncertain; visits should respect nearby communities and religious sites rather than treating them as safari scenery.
155|Great Rann of Kutch|23.8340|69.5220|BHJ|2|16|Gujarat desert & heritage|desert|White salt landscape; sunset; Hodka village crafts; moonlight photography|Now included after lifting the desert exclusion. Salt-surface conditions depend on rain and evaporation, and access needs the current Rann permit/checkpoint process. Festival camps are one accommodation option, not the only way to experience the landscape. Border extensions need separate eligibility checks.
156|Little Rann and Wild Ass Sanctuary|23.1300|71.8900|AMD|2.5|16|Gujarat desert & heritage|desert|Authorized jeep safari; Indian wild ass; flamingo and raptor birding; salt-worker landscape by invitation|A wildlife-focused desert addition, distinct from the Great Rann's white-salt spectacle. Protected-area entry and a suitable guide/vehicle are required. Winter bird interest is strong but sightings and accessible terrain depend on current water and sanctuary conditions.
157|Dholavira and Khadir|23.8860|70.2130|BHJ|4|12|Gujarat desert & heritage|desert|Harappan city remains; ancient reservoirs; Khadir landscape; salt-flat photography|Archaeological engineering and dramatic open landscapes may appeal more than a conventional museum visit. Road-edge viewpoints and salt access are not interchangeable with free driving across the Rann. Plan for intense sun and sparse services outside the winter season.
158|Patan and Modhera|23.8500|72.1260|AMD|2.5|8|Gujarat desert & heritage|desert|Rani ki Vav stepwell; Modhera Sun Temple; Patola weaving by arrangement; detailed architectural photography|A concentrated architecture-and-craft option rather than a desert adventure. Individual sites and workshops have their own admission and camera arrangements. Winter is comfortable for outdoor stonework photography; summer heat can make midday visits strenuous.
159|Velavadar grasslands|22.0260|72.0500|AMD|3|16|Gujarat desert & heritage|desert|Authorized blackbuck safari; grassland birds; harrier roost observation where allowed; landscape photography|A different habitat from Gir, with open grasslands and seasonal birding. Access and wildlife activity are time-dependent; a known species does not guarantee a sighting. Confirm park opening and the permitted viewing route before arranging a sunrise or evening outing.
160|Patiala|30.3398|76.3869|IXC|1.5|12|Punjab & Haryana|plains|Qila Mubarak access where open; Baradari Gardens; Dukhniwaran Sahib; Punjabi food and old streets|A culture-and-food addition beyond Amritsar. Conservation may limit parts of the palace complex, so check current access. Useful for street photography and living Sikh/Punjabi culture without making a large museum visit compulsory.
161|Kapurthala and Jalandhar|31.3800|75.3800|ATQ|1.5|10|Punjab & Haryana|plains|Jagatjit Palace exterior where permitted; Moorish Mosque; Elysee Palace area; Jalandhar local food|Architecture and town life provide a quieter Punjab option. Some buildings serve institutions rather than unrestricted tourism, so exterior viewing may be the realistic experience. Obtain permission for campus/interior photography rather than assuming a palace name means open access.
162|Harike Wetland|31.1600|74.9700|ATQ|1.5|8|Punjab & Haryana|plains|Winter waterbird watching; permitted bund trails; confluence landscapes; local naturalist outing|A particularly good outdoor Punjab addition. Use the authorized access point and verify sanctuary arrangements. Boating requires special permission and is not assumed included; winter water levels and migration affect what you will see.
163|Bathinda and rural Malwa|30.2110|74.9450|IXC|4|10|Punjab & Haryana|plains|Qila Mubarak; lakeside walks; Takht Damdama Sahib region; Punjabi food|Useful for a less obvious Punjab cultural segment. It has more local-life and devotional appeal than mountain-style adventure. Rural visits should be arranged by invitation, with sacred-site rules and photography preferences respected.
164|Chandigarh|30.7333|76.7794|IXC|.5|10|Punjab & Haryana|plains|Rock Garden; Sukhna Lake; Capitol architecture through approved visits; neighborhood cafes|A designed-city and green-space contrast to older towns. Good for architecture and an easy outdoor day, not a substitute for mountain adventure. Capitol-complex access and photography can require advance arrangements; the airport gateway is separate from local sightseeing.
165|Kurukshetra|29.9695|76.8783|IXC|2|8|Punjab & Haryana|plains|Brahma Sarovar; Jyotisar; sacred tanks and temple settings; evening photography|Select for religious history and water-reflection photography rather than adrenaline. Festival dates greatly change crowds and the devotional experience. Keep museum attractions optional, consistent with the user's preferences.
166|Pinjore and Morni Hills|30.8000|76.9160|IXC|1.5|8|Punjab & Haryana|hill|Pinjore Gardens; Morni hill viewpoints; Tikkar Tal; permitted nature walks|A lower-hill outing with gardens and lakes, useful for a quieter scenic stop. Verify legal trails and boating arrangements; hill roads and reservoir access are separate from unrestricted off-roading or wild camping.
167|Fort Kochi and Mattancherry|9.9650|76.2420|COK|1.25|12|Kerala|coast|Waterfront fishing-net views; Mattancherry streets; heritage lanes; Kerala food and performing arts by arrangement|Adds a focused Kerala city choice rather than only using Kochi as a gateway. Strong street photography and coastal atmosphere. Performance tickets and religious-site admissions are separate; ferry and waterfront access need current checking.
168|Wayanad|11.6850|76.1320|CCJ|3.5|24|Kerala|ghats|Edakkal rock shelter; plantation walks; permitted forest safari; ridge viewpoints|A focused option split out from the earlier broad Munnar–Wayanad–Thekkady cluster. Forest access and individual peaks can close; do not assume popular trek names are currently open. Edakkal is a rock shelter with carvings, not Meghalaya-style adventure caving.
169|Thekkady and Periyar|9.6030|77.1610|COK|5|24|Kerala|ghats|Authorized Periyar nature programs; lake boat outing; spice-country walks; guided forest interpretation|A focused wildlife and forest alternative, split from the earlier broad Kerala cluster. Choose actual authorized programs and confirm age/fitness/permit conditions. Wildlife sightings are uncertain, and a general entry ticket does not grant independent access to every trail.
170|Vagamon and Idukki|9.6870|76.9050|COK|3.5|16|Kerala|ghats|Meadow and ridge walks; pine-country scenery; Idukki viewpoints; paragliding only with an authorized operating provider|Strong personal fit for green hills and photography. Adventure offerings depend on wind, approvals and operator availability. Reservoir/dam visits can have distinct security and opening rules; scenic roads do not imply open access to dam structures.
171|Athirappilly and Vazhachal|10.2850|76.5700|COK|1.5|8|Kerala|ghats|Athirappilly waterfall viewpoints; Vazhachal; river-and-forest photography; permitted forest-country outing|Waterfall power varies through the year; the monsoon spectacle comes with greater access and weather restrictions. Use authorized viewing paths and follow closure notices. Do not assume swimming below the falls is permitted or appropriate.
172|Kumarakom and Vembanad|9.6170|76.4300|COK|2.5|16|Kerala|coast|Small-canal kayaking; Vembanad water views; bird sanctuary where open; village food and canoe outings|A focused backwater option distinct from the earlier combined Kerala coast cluster. Small craft can provide a more active experience than a mandatory houseboat stay. Confirm authorized departure points, conditions and wildlife access; boat choice and cost are not bundled into transport totals.
173|Varkala|8.7379|76.7163|TRV|1.5|16|Kerala|coast|Cliff-top coastal walks; beach time; surfing lessons when conditions suit; Janardanaswamy temple surroundings|A separate coastal choice with activity and scenery rather than nightlife as the main draw. Surf conditions, lifeguard guidance and access to unstable cliff sections matter. The original broad Kerala coast cluster overlaps this focused destination; avoid duplicating visit days unintentionally.
174|Munroe Island and Kollam|8.9970|76.6110|TRV|2|16|Kerala|coast|Guided narrow-canal paddling; backwater village views; Ashtamudi landscapes; local food|Good match for hands-on water exploration and early-light photography. Tides, village waterways and boat permissions determine the route. A tranquil photo does not guarantee every canal is navigable year-round; use a local guide for a suitable legal outing.
175|Bekal and Kasaragod|12.3930|75.0340|CNN|2|12|Kerala|coast|Bekal Fort; beach landscapes; backwaters around Valiyaparamba by arrangement; coastal villages|A quieter northern Kerala alternative with outdoor architecture and sea views. Water activity and beach conditions are seasonal. Strong if the trip needs a coastal segment with less emphasis on a large resort or busy city.
176|Kannur and Thalassery|11.8740|75.3700|CNN|.75|16|Kerala|coast|Theyyam through a verified local calendar; Thalassery food; fort and beach walks; coastal photography|Living culture and food can make this more distinctive than simply another beach. Theyyam is sacred and calendar-specific: follow local photography rules and never assume a performance is available daily. Beach driving is only a lead where currently legal, not a general rental-vehicle entitlement.
177|Silent Valley and Palakkad hills|11.0780|76.4380|CJB|3|24|Kerala|ghats|Authorized Silent Valley visit; rainforest interpretation; Palakkad landscape; permitted village walks|A nature-focused alternative to busy hill towns. Park entry, vehicles, operating routes and any trekking require current forest-department arrangements. Do not assume free hiking inside protected rainforest or guaranteed primate sightings.
178|Thiruvananthapuram and Kovalam|8.5241|76.9366|TRV|.5|16|Kerala|coast|Kovalam coast; Poovar estuary boat outing where authorized; city food; Padmanabhaswamy temple area|A southern Kerala city-and-water option. Temple interior eligibility and dress rules must be checked personally; foreign-visitor status alone does not establish religious-site admission. Sea and estuary outings depend on conditions and lawful operators.
179|Mysuru and Srirangapatna|12.2958|76.6394|BLR|3.5|16|Karnataka|ghats|Mysore Palace; Chamundi Hills; Srirangapatna river-island heritage; market food and photography|A clear standalone Karnataka cultural destination with accessible outdoor viewpoints. Palace illumination is schedule-specific, not a nightly guarantee. Ranganathittu birding is a separate protected-site outing with its own boat and entry arrangements.
180|Coorg and Kodagu|12.4240|75.7380|IXE|4|24|Karnataka|ghats|Coffee-estate walks; Madikeri viewpoints; permitted ridge trek; river activity through a qualified provider|A focused coffee-and-hills choice split from the earlier broad Western Ghats entry. Trek peaks need actual permits and opening checks. Rafting is flow-dependent and may not be a dry-season option; independent access to plantation land is not assumed.
181|Badami, Aihole and Pattadakal|15.9140|75.6760|HBX|3|16|Karnataka|ghats|Badami rock-cut temples; Agastya Lake; Pattadakal temple complex; Aihole architecture|Rock landscapes and outdoor stone architecture offer a strong photography trip. These caves are architectural sites rather than expedition caving. Climbing requires a competent local provider and legal access; temple admission and photography rules remain site-specific.
182|Udupi and Malpe|13.3409|74.7421|IXE|1.5|16|Karnataka|coast|Malpe coast; Udupi food; Krishna temple area; St Mary's Islands ferry if operating|An active coast-and-food option. Island ferries and water activities depend on weather and official operations, especially during monsoon. Religious-site eligibility and dress rules need checking; do not infer them from passport type alone.
183|Murudeshwar and Honnavar|14.0940|74.4850|GOX|5|16|Karnataka|coast|Murudeshwar seafront Shiva complex; Honnavar estuary boating; coastal viewpoints; Netrani diving through an operating center|Strong blend of temple scenery and water activities. Offshore diving has separate sea-condition, provider and eligibility requirements. Use the actual approved dive site and schedule; an attractive coastline does not guarantee good underwater visibility.
184|Jog Falls and Sharavathi country|14.2290|74.8120|HBX|4|16|Karnataka|ghats|Jog Falls viewpoints; Sharavathi backwater scenery; permitted forest walks; village stays|A strong waterfall/landscape lead whose appearance depends on rainfall and releases. December can be far less dramatic than monsoon photographs. Verify current viewpoint and forest access; kayaking is an operator-specific possibility, not automatically available throughout the reservoir.
185|Ooty and Coonoor|11.4100|76.6950|CJB|3.5|24|Tamil Nadu|hill|Nilgiri Mountain Railway; Coonoor tea-country walks; ridge viewpoints; permitted forest outings|A mountain-and-rail alternative in South India. Train reservations and actual services need checking, and tea production is seasonal. Some famous viewpoints are vehicle-access stops, while genuine forest trails have separate permission requirements.
186|Kodaikanal|10.2381|77.4892|IXM|3.5|24|Tamil Nadu|hill|Lake and ridge walks; Coaker's Walk; Pillar Rocks viewpoints; permitted forest trails|Strong landscape and walking fit, with cooler nights than the surrounding plains. Research current forest-route access; popular social-media viewpoints do not imply legal unrestricted entry. Nearby multi-day trekking needs a separate operator and permit assessment.
187|Madurai|9.9252|78.1198|IXM|.5|16|Tamil Nadu|coast|Meenakshi temple area; old-city food; Thirumalai Nayakkar Palace; market photography|A major living-temple and food destination rather than simply a transit stop. Interior eligibility, phone/camera restrictions and dress rules are site-specific. The city is warm even in winter; plan the most exposed walking outside midday when possible.
188|Rameswaram and Dhanushkodi|9.2880|79.3130|IXM|4|16|Tamil Nadu|coast|Ramanathaswamy temple; Dhanushkodi landscapes; Pamban viewpoints; seafront pilgrimage atmosphere|A strong sacred-and-coastal addition, with photogenic open-water landscapes. Dhanushkodi access may be controlled or weather-limited. Do not enter restricted railway structures or assume swimming is permitted everywhere; island/coastal winds can be substantial.
189|Kanyakumari|8.0883|77.5385|TRV|3|12|Tamil Nadu|coast|Seafront sunrise; Vivekananda Rock ferry if operating; coastal monuments; nearby Padmanabhapuram Palace|Useful for dramatic southern-tip light and cultural scenery. Weather and queues affect ferry plans; sunrise and sunset visibility depend on cloud. Palace access and the offshore excursion are separate activities with their own tickets and schedules.
190|Mahabalipuram and Chennai coast|12.6208|80.1945|MAA|1.5|16|Tamil Nadu|coast|Shore Temple; Five Rathas; rock reliefs; coastal walking|Outdoor stonework, sea light and compact heritage make a strong photography combination. This cluster overlaps Chennai only as a regional gateway, not a duplicate city visit. Monsoon/cyclone-season conditions can affect exposed coastal outings.
191|Puducherry and Auroville|11.9416|79.8083|MAA|3.5|16|Tamil Nadu & Puducherry|coast|French Quarter streets; promenade; local food; Auroville through official visitor arrangements|A slower streets-and-coast segment. Auroville's visitor center and Matrimandir inner access are different experiences; the latter cannot be assumed from a casual arrival. Cycling and surf lessons are activity leads subject to current conditions.
192|Thanjavur and Kumbakonam|10.7870|79.1378|TRZ|1.5|20|Tamil Nadu|coast|Brihadisvara temple; Darasuram; Gangaikonda Cholapuram; Kumbakonam temple streets|A focused Chola architecture and living-temple region, with detailed sculpture and courtyard photography. Choose a few meaningful sites rather than treating every temple as compulsory. Individual inner-sanctum and camera restrictions vary.
193|Chennai|13.0827|80.2707|MAA|.5|12|Tamil Nadu|coast|Mylapore streets; Kapaleeshwarar temple area; Marina waterfront; food and music events by calendar|A cultural city stop with less direct adventure than the hill and island choices. December music events are date-and-ticket specific. Coastal weather can be unsettled during the northeast-monsoon period; don't assume dry winter conditions from North India apply here.
194|Tiruvannamalai|12.2253|79.0747|MAA|4|16|Tamil Nadu|coast|Arunachaleswarar temple; Arunachala surroundings; legal hill/forest paths; devotional town walks|A strong sacred-atmosphere option if the religious interest is central. Hill climbing and forest access are subject to permissions and closures. Full-moon pilgrimage dates create a very different crowd experience; do not assume a quiet village-style stay.
195|Valparai and Anamalai foothills|10.3270|76.9550|CJB|3.5|24|Tamil Nadu|ghats|Tea-country landscapes; permitted forest-edge walks; Anamalai naturalist outings; reservoir viewpoints where open|Good wildlife-and-motorcycle scenery for a later lawful transport plan. Elephants and other wildlife share the landscape; avoid independent night wildlife pursuit. Protected-area safari/forest visits are separate from driving a public road through plantations.
196|Yercaud|11.7750|78.2090|BLR|5|16|Tamil Nadu|hill|Shevaroy hill views; lake surroundings; coffee-country walks; ridge photography|A gentler hill alternative with short walks rather than a major expedition. Estate access needs permission and waterfall volume is seasonal. Better chosen for a relaxed scenic segment than expecting the scale of Himalayan trekking.
197|Hyderabad|17.3850|78.4867|HYD|.5|16|Telangana & Andhra|ghats|Golconda Fort; Charminar lanes; Qutb Shahi tomb landscape; food exploration|Excellent food and architectural street photography. Fort performances, interior access and evening events need actual schedules. Nearby outdoor bouldering is a specialist activity requiring a qualified local group and legal land access, not an assumed city attraction.
198|Warangal and Ramappa|17.9689|79.5941|HYD|3.5|16|Telangana & Andhra|ghats|Ramappa temple; Warangal Fort; Thousand Pillar Temple; Pakhal landscape|A less obvious heritage-and-lake contrast to Hyderabad. Choose outdoor architecture and countryside photography over a dense museum route. Lake/forest access and boating are site-specific; current road and monument arrangements need checking.
199|Gandikota|14.8140|78.2840|BLR|5.5|16|Telangana & Andhra|ghats|Pennar gorge viewpoints; fort remains; sunrise and sunset; guided local scrambling where permitted|One of the strongest South India additions for dramatic landscape photography. Cliff edges are exposed; viewpoints and legal camping need local verification. Do not infer unrestricted climbing or river access from the canyon's popularity.
200|Belum Caves and Kurnool country|15.1020|78.1110|BLR|5.5|12|Telangana & Andhra|ghats|Authorized Belum tourist cave route; rock formations; local stone landscapes; Kurnool heritage as an optional extension|A substantial underground sightseeing option, distinct from Meghalaya expedition caving. Stay within operating tourist passages; heat, ventilation and any guide requirements matter. Gandikota and Belum are separate stops that can be compared rather than automatically duplicated.
201|Araku Valley and Borra Caves|18.3270|82.8800|VTZ|3.5|24|Telangana & Andhra|ghats|Borra cave tourist route; hill and coffee landscapes; valley train when operating; invited community craft visits|Very strong mix of caves, hills and rail scenery. Actual train operations, cave access and estate visits must be confirmed. Approach community culture through local guides and permission rather than treating residents as a photographic exhibit.
202|Visakhapatnam coast|17.6868|83.2185|VTZ|.5|16|Telangana & Andhra|coast|Rushikonda area; coastal viewpoints; beach walks; food and hilltop scenery|A scenic coastal city option and Araku gateway. Sea conditions and beach safety vary; surfing or water sports need an authorized operating provider. Museum attractions are optional, consistent with the user's preference for outdoor experiences.
203|Tirupati and Tirumala|13.6288|79.4192|TIR|.5|16|Telangana & Andhra|ghats|Tirumala pilgrimage through official arrangements; temple-town atmosphere; permitted foothill walks; local food|Choose for a specific devotional goal. Darshan booking, identity/declaration requirements for foreign/non-Hindu visitors, dress and access rules need official confirmation. Document status alone is not proof of religious eligibility or a guaranteed ticket.
204|Srisailam and Nallamala|16.0730|78.8680|HYD|5|20|Telangana & Andhra|ghats|Mallikarjuna temple; Krishna gorge views; authorized reservoir outings; permitted forest-country travel|Sacred atmosphere and river landscapes are the main draws. Nallamala protected-forest routes, boating and dam access can be controlled and seasonal. A public road through forest does not grant independent off-road trekking permission.
205|Puri and Konark|19.8135|85.8312|BBI|1.5|20|Odisha|coast|Konark Sun Temple; Puri beach; coastal villages; Jagannath temple surroundings|A strong architecture-and-coast addition. Jagannath temple interior has religious eligibility restrictions and foreign-visitor admission must not be assumed. Konark and the seafront still offer substantial outdoor interest. Cyclone-season weather and sea conditions require current checking.
206|Chilika and Mangalajodi|19.8480|85.4490|BBI|2|24|Odisha|coast|Guided wetland boat birding; Mangalajodi community outings; lagoon landscapes; lawful dolphin-viewing trips at suitable locations|Excellent match for boat-based wildlife photography, especially winter birds. Use responsible operators and maintain wildlife distance. Dolphin viewing and Mangalajodi birding occur in different lagoon areas; don't imply every excursion includes both.
207|Bhitarkanika|20.7300|86.8760|BBI|4|24|Odisha|coast|Authorized mangrove boat safari; crocodile and bird observation; permitted forest trails; creek landscapes|A strong alternative wetland ecosystem to conventional jeep safaris. Entry and authorized boats must be arranged; seasonal closure dates and tide affect the actual route. This is crocodile habitat, not a swimming or independent kayaking destination.
208|Similipal and Baripada|21.7500|86.3700|BBI|5|24|Odisha|ghats|Authorized forest safari; waterfalls when open; sal-forest landscapes; local cultural interpretation|A less obvious forest-and-waterfall destination with strict park operations. Reserve the permitted route/vehicle and check season, conservation closures and accommodation. Do not promise tiger sightings or access to every waterfall listed online.
209|Sundarbans|22.1000|88.7500|CCU|4|24|Bengal & eastern forests|coast|Authorized estuary boat itinerary; mangrove and bird photography; watchtowers where open; invited village visits|Distinctive tidal wildlife landscapes, better appreciated as an ecosystem than a guaranteed tiger trip. Forest entry and boat permits must be arranged for the exact route; foreign-passport paperwork may differ. No independent mangrove walking or swimming is assumed.
210|Kolkata|22.5726|88.3639|CCU|.75|16|Bengal & eastern forests|coast|Hooghly riverfront; flower market; old neighborhoods; Bengali food and cultural events|A living-city and street-photography contrast to the forest and mountain options. Ask before close portraits in working markets. Performances, ferries and major events depend on actual schedules; museums remain optional.
211|Bodh Gaya, Rajgir and Nalanda|24.6960|84.9910|GAY|.5|24|Bihar & Jharkhand|plains|Mahabodhi temple setting; international monasteries; Rajgir hills; Nalanda ruins|A broad Buddhist pilgrimage and landscape cluster. The pin represents Bodh Gaya; Rajgir and Nalanda are separate regional excursions, not walkable nearby sights. Strong for sacred atmosphere and architecture; individual temple/site entry and camera rules vary.
212|Valmiki Tiger Reserve|27.3350|84.1600|PAT|7|24|Bihar & Jharkhand|plains|Authorized forest safari; Gandak river landscapes; birding; permitted nature interpretation|An offbeat wildlife option rather than a guaranteed big-cat encounter. The long regional approach is an editorial allowance, not a timetable. Verify park routes, season, lodging and any river activity authorization before selecting this over other reserves.
213|Ranchi, waterfalls and Netarhat|23.3441|85.3096|IXR|.5|24|Bihar & Jharkhand|ghats|Dassam and Hundru viewing areas; Ranchi plateau; Netarhat sunrise country; local food|A broad plateau-and-waterfall alternative with distinct places spread across the region. Flow changes seasonally and safe authorized viewing routes matter. Netarhat requires a separate outing; the city pin is a representative gateway, not a claim that all sights are nearby.
214|Bastar and Chitrakote|19.2070|81.7000|RPR|6|24|Chhattisgarh & central hills|ghats|Chitrakote waterfall viewpoints; Tirathgarh when open; permitted Kanger Valley visits; invited local craft encounters|A dramatic waterfall and forest lead, with current local access conditions essential. Cave and forest visits require official arrangements. Do not assume every rural road or community visit is accessible; use current district guidance and respectful local hosts.
215|Sirpur and Barnawapara|21.3520|82.1830|RPR|2|16|Chhattisgarh & central hills|ghats|Sirpur archaeological remains; Mahanadi landscapes; authorized Barnawapara safari; local village setting|A culture-and-forest option with less tourist-city bustle. Archaeological access and wildlife permits are separate arrangements. Wildlife is uncertain, and independent wandering through sanctuary habitat is not assumed.
216|Amarkantak|22.6750|81.7590|JLR|5|16|Chhattisgarh & central hills|ghats|Narmada source temples; forest-country viewpoints; ancient temple complex; authorized nature walks|A sacred-source and forested-hill destination with a quieter pace. The route and temperature differ from lowland central India. Check specific trail permissions and approach the temple context as living worship rather than only a photo location.
217|Lakshadweep: Agatti and Bangaram|10.8560|72.1850|AGX|1.5|32|Islands|island|Approved-island snorkeling; diving with a qualified center; lagoon paddling; beach photography|A high-interest water-focused extension that needs advance entry permission and island-specific foreign-visitor eligibility confirmation. Official guidance contains tourist-visa wording, so do not assume document status alone resolves admission. Transfers depend on sea conditions and approved lodging/boat arrangements.
'''

def augment(data):
    sources={
      'rajasthan':('Rajasthan Tourism destination directory','https://www.tourism.rajasthan.gov.in/tourist-destinations.html'),
      'punjab':('Punjab / Harike visitor guidance','https://www.incredibleindia.gov.in/en/punjab/amritsar/harike-wetland-and-bird-sanctuary'),
      'patiala':('Patiala official tourist places','https://patiala.nic.in/tourist-places/'),
      'tn':('Tamil Nadu Tourism','https://www.tamilnadutourism.tn.gov.in/'),
      'ap':('Andhra Pradesh Tourism','https://tourism.ap.gov.in/'),
      'telangana':('Telangana Tourism','https://tourism.telangana.gov.in/'),
      'odisha':('Odisha Tourism','https://odishatourism.gov.in/'),
      'bengal':('West Bengal Tourism','https://wbtourism.gov.in/'),
      'bihar':('Bihar Tourism','https://tourism.bihar.gov.in/'),
      'jharkhand':('Jharkhand Tourism','https://tourism.jharkhand.gov.in/'),
      'chhattisgarh':('Chhattisgarh Tourism','https://tourism.cgstate.gov.in/'),
      'lakshadweep':('Lakshadweep official entry-permit instructions','https://lakshadweep.gov.in/tourism/entry-permit/'),
      'laknew':('Lakshadweep permit portal migration notice, October 2026','https://lakshadweep.gov.in/notice/from-15th-october-2026-onwards-all-e-permit-services-will-be-available-through-the-new-portal/'),
      'laktravel':('Lakshadweep official access and transport information','https://lakshadweep.gov.in/how-to-reach/'),
      'laktour':('Lakshadweep official tourism / foreign-visitor wording','https://lakshadweep.gov.in/tourism/tourist-packages/'),
      'rann':('Gujarat Tourism Great Rann visitor information','https://gujarattourism.com/kutch-zone/kutch/great-rann-of-kutch.html'),
    }
    data['sources'].update({k:{'label':v[0],'url':v[1]} for k,v in sources.items()})
    data['climates']['desert']={'name':'Arid northwest planning band; nights much cooler','source':'imd','low':[8,11,17,23,27,29,27,26,24,19,13,9],'high':[23,27,33,38,41,40,36,34,35,34,29,24]}
    data['climates']['southeast']={'name':'Southeast-coast planning band; northeast-monsoon influence','source':'imd','low':[21,22,24,26,27,27,26,26,25,24,23,22],'high':[29,31,33,35,37,36,35,34,33,31,29,28]}
    data['permits']['island']={'level':'permit','label':'Entry permit + island eligibility','text':'Lakshadweep entry permission is required. Confirm the exact approved island, foreign-visitor eligibility, visa wording and approved accommodation before booking. The official site announced an e-permit portal migration from 15 October 2026; follow the current official notice rather than an old portal bookmark.','links':['lakshadweep','laknew','laktour','nepermit']}
    data['permits']['rann']={'level':'check','label':'Rann / border access check','text':'Confirm current White Rann permit, identity and checkpoint requirements through official local guidance. Foreign-visitor access to frontier extensions is not assumed. Sanctuary outings need their own permissions.','links':['rann','gujarat','nepermit']}
    hubraw='''JAI|Jaipur · JAI / JP|26.824|75.812
UDR|Udaipur · UDR / UDZ|24.617|73.896
JDH|Jodhpur · JDH / JU|26.251|73.048
JSA|Jaisalmer · JSA / JSM|26.889|70.865
BKB|Bikaner rail gateway · BKN|28.015|73.317
BHJ|Bhuj · BHJ / BHUJ|23.287|69.670
TRV|Thiruvananthapuram · TRV / TVC|8.482|76.920
CCJ|Kozhikode · CCJ / CLT|11.136|75.955
CNN|Kannur · CNN / CAN|11.919|75.548
CJB|Coimbatore · CJB / CBE|11.030|77.043
IXM|Madurai · IXM / MDU|9.834|78.094
TRZ|Tiruchirappalli · TRZ / TPJ|10.765|78.709
HYD|Hyderabad · HYD / SC|17.240|78.429
VTZ|Visakhapatnam · VTZ / VSKP|17.722|83.224
TIR|Tirupati · TIR / TPTY|13.632|79.543
BBI|Bhubaneswar · BBI / BBS|20.245|85.818
GAY|Gaya · GAY / GAYA|24.744|84.951
PAT|Patna · PAT / PNBE|25.591|85.088
IXR|Ranchi · IXR / RNC|23.314|85.322
RPR|Raipur · RPR / R|21.181|81.738
AGX|Agatti · AGX|10.824|72.176'''
    for line in hubraw.splitlines():
        code,name,lat,lon=line.split('|');data['nodes'].append(dict(id=code,name=name,lat=float(lat),lon=float(lon),hub=True))
    srcby={'Rajasthan':'rajasthan','Gujarat desert & heritage':'gujarat','Punjab & Haryana':'incredible','Kerala':'kerala','Karnataka':'kar','Tamil Nadu':'tn','Tamil Nadu & Puducherry':'tn','Telangana & Andhra':'ap','Odisha':'odisha','Bengal & eastern forests':'bengal','Bihar & Jharkhand':'bihar','Chhattisgarh & central hills':'chhattisgarh','Islands':'lakshadweep'}
    for row in RAW.strip().splitlines():
        ident,name,lat,lon,hub,access,visit,region,climate,acts,notes=row.split('|');i=int(ident);activities=acts.split('; ');source=srcby[region]
        if i in [187,188,190,191,192,193,194,202,205,206,207]:climate='southeast'
        if i==160:source='patiala'
        if i==162:source='punjab'
        if i in [197,198]:source='telangana'
        if i==213:source='jharkhand'
        permit='general'
        if i in [147,148,149,154,156,159,162,169,177,195,206,207,208,209,212,214,215]:permit='forest'
        if i in [155,157]:permit='rann'
        if i==217:permit='island'
        words=(acts+' '+notes).lower();tags=[]
        for tag,pat in [('Hikes','walk|trek|ridge|hill|climb'),('Mountains','mountain|hill|ridge|ghat'),('Water','water|river|lake|lagoon|boat|coast|beach|paddl|snork|diving'),('Caves','cave|canyon|gorge'),('Wildlife','safari|wildlife|bird|forest|tiger|leopard'),('Culture','temple|fort|palace|food|heritage|street|craft'),('Night skies','night.sky|moonlight'),('Desert','desert|dune|salt')]:
            if re.search(pat,words):tags.append(tag)
        links=[]
        if i in [155,157]:links.append('rann')
        if i==217:links+=['laktravel','laktour','laknew']
        d=dict(id=ident,num=i,name=name,lat=float(lat),lon=float(lon),hub=hub,access=float(access),visitHours=float(visit),days=float(visit)/8,region=region,source=source,description=acts+'. '+notes,activities=activities,tags=tags,fit='A' if i in [141,142,143,147,148,150,154,155,156,157,168,169,170,171,174,175,177,180,181,183,184,185,186,188,195,199,200,201,206,207,208,209,214,217] else 'B',climate=climate,permit=permit,closedMonths=[],decCaution=False,seasonNote='Nationwide expansion · December generally a seasonal candidate; specific operations unverified.',links=links,country='India',visited=i in [138,139,140])
        data['destinations'].append(d);data['nodes'].append(dict(id=ident,name=name,lat=float(lat),lon=float(lon),hub=False))
    def edge(a,b,mode,h,lo,hi,source='incredible',basis='person',note='Explicit corridor; time and fares are editorial planning allowances. Recheck actual services, terminals and operating dates.',evidence='Editorial corridor / budget allowance'):
        data['edges'].append(dict(id='e'+str(len(data['edges'])),a=a,b=b,mode=mode,hours=h,low=lo,high=hi,source=source,note=note,basis=basis,months=list(range(1,13)),evidence=evidence,access=False))
    for d in data['destinations'][137:]:
        h=d['access'];private=d['num'] in [143,154,155,156,157,159,177,207,208,209,212,214,217]
        low=4000 if d['num']==217 else round(max(600 if private else 100,h*(500 if private else 150))/50)*50
        high=12000 if d['num']==217 else round(max(1200 if private else 250,h*(900 if private else 320))/50)*50
        edge(d['id'],d['hub'],'boat' if d['num']==217 else 'road',h,low,high,d['source'],'vehicle' if private else 'person','Regional gateway approach; hotel transfers, local sightseeing and activity fees excluded. '+('Private vehicle / charter allowance shared at up to 4 travelers.' if private else 'Public/shared-road budget allowance; exact service unverified.'))
    # Explicit airport leads, with estimates rather than fictitious dated quotes.
    flights='''DEL JAI 1 3000 7000
DEL UDR 1.4 4500 9500
DEL JDH 1.4 4000 9000
DEL JSA 1.6 5500 13000
BOM JAI 1.8 4500 9500
BOM UDR 1.5 4000 9000
BOM JDH 1.6 4500 9500
BOM BHJ 1.6 5000 11000
DEL HYD 2.2 5000 10500
BOM HYD 1.5 4000 8500
BLR HYD 1.2 3500 7500
MAA HYD 1.3 3500 7500
BLR TRV 1.3 4000 8500
COK TRV .8 3000 6500
BLR CCJ 1.2 3500 7500
BLR CNN 1.2 3500 7500
BLR CJB 1 3000 7000
MAA CJB 1.1 3000 7000
MAA IXM 1.3 3500 7500
BLR IXM 1.4 4000 8500
MAA TRZ 1 3000 7000
BLR TRZ 1.2 3500 7500
HYD VTZ 1.2 3500 7500
MAA VTZ 1.3 3500 8000
HYD TIR 1.2 3500 7500
BLR TIR 1 3000 7000
DEL BBI 2.2 5000 10500
CCU BBI 1.1 3000 7000
HYD BBI 1.5 4000 8500
CCU GAY 1.1 3500 8000
DEL PAT 1.8 4000 9000
CCU PAT 1.2 3500 7500
DEL IXR 1.9 4500 9500
CCU IXR 1.1 3000 7000
DEL RPR 1.9 4500 9500
HYD RPR 1.3 3500 7500
COK AGX 1.5 6000 13000'''
    for row in flights.splitlines():
        a,b,h,lo,hi=row.split();edge(a,b,'flight',float(h),int(lo),int(hi),'laktravel' if b=='AGX' else 'air',evidence='Published route lead; time / fare allowance; dated schedule unverified')
    rail='''DEL JAI 4.5 650 1400
JAI UDR 6.5 900 1900
JAI JDH 5.5 750 1700
JDH JSA 6 650 1500
JAI BKB 6.5 700 1600
BKB JSA 6 650 1500
UDR JDH 12 1000 2200
AMD BHJ 7 750 1800
AMD UDR 5.5 600 1500
JAI AGR 4 550 1300
JAI DEL 4.5 650 1400
MAA IXM 7 850 1800
MAA TRZ 5.5 700 1600
CJB COK 4 500 1200
COK TRV 4 600 1400
CCJ COK 4.5 550 1300
CNN CCJ 2 300 800
BLR CJB 6 700 1600
MAA TIR 3 450 1000
HYD VTZ 11 1000 2200
VTZ BBI 7 700 1700
CCU BBI 7 800 1700
PAT GAY 2.5 350 900
VNS PAT 5 650 1400
PAT IXR 8 850 1800
RPR JLR 8 850 1900
HYD RPR 12 1100 2300'''
    for row in rail.splitlines():
        a,b,h,lo,hi=row.split();edge(a,b,'train',float(h),int(lo),int(hi),'rail')
    local='''138 145 3
138 146 4
138 147 3.5
138 149 2.5
138 152 3
139 140 2.5
139 150 2.5
139 151 3
141 142 5
141 154 3.5
142 143 1.5
145 146 4
146 153 1
147 148 4
150 154 2.5
151 158 3
155 157 4
156 158 2.5
160 164 1.5
160 163 3
161 162 1.5
052 162 1.5
052 161 1.5
164 165 2
164 166 1.5
167 171 2
167 172 2
168 176 3
168 177 4
169 170 2
170 135 3
172 174 3
173 174 1
173 178 1.5
175 176 2
179 180 3
179 185 4
179 168 3.5
181 131 3
182 183 2.5
183 184 2
183 132 1.5
185 195 5
186 187 3.5
187 188 4
187 189 4.5
190 191 2
191 192 4
192 187 3
193 190 1.5
194 191 2.5
197 198 3.5
197 204 5
199 200 1.5
201 202 3.5
203 193 3
205 206 2
205 207 5
207 208 5
211 212 9
214 215 7
125 216 7'''
    for row in local.splitlines():
        a,b,h=row.split();h=float(h);edge(a,b,'road',h,round(max(200,h*150)/50)*50,round(max(500,h*350)/50)*50)
    edge('UDR','JDH','road',4.5,600,1400,'rajasthan',note='Intercity road budget allowance; rail options may be indirect. Verify actual public services and local terminal transfers.')
    data['version']=2
    return data
