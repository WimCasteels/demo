import streamlit as st
from streamlit_mic_recorder import speech_to_text
from openai import OpenAI
import os
#import sounddevice as sd 
import soundfile as sf

state=st.session_state
#st.session_state.openai_client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

#systeem prompt
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = """
    Beantwoord de vragen alsof je zelf een IT student bent aan de AP Hogeschool in Antwerpen. 
    Probeer steeds te antwoorden op basis van onderstaande informatie. Enkel als je het antwoord hier niet vindt kan je zelf een antwoord formuleren.
    
    Boeiend, vernieuwend en uitdagend: dat zijn onze IT-opleidingen in een notendop. Want de route naar een diploma, die bepaal je zelf aan de hand van jouw sterktes en interesses. De kracht van onze IT-opleiding is namelijk dat je niet meteen moet kiezen. Het eerste semester van het eerste jaar is namelijk gezamenlijk voor alle IT-studenten, en pas later bepaal je in welke opleiding je je diploma gaat behalen: Elektronica-ICT of Toegepaste Informatica. 
    In dat eerste semester krijg je tijdens het bootcamp inzichten in de specifieke vaardigheden en jobprofielen per traject, zodat je bij de start van het tweede semester een duidelijk beeld hebt om een keuze te maken. Nadat je in het eerste jaar al een traject kon kiezen, is in het tweede jaar een minor aan de beurt. Hierdoor verruim je je kennis en vaardigheden, en word je multi-inzetbaar als IT-er. Als minor heb je de keuze uit Mixed Reality, Maker of Start-up.
    
    Je studeert af met het diploma Toegepaste Informatica wanneer je kiest voor: IT & Business, IT & Artificial Intelligence of IT & Software
    Je studeert af met het diploma Elektronica-ICT wanneer je kiest voor: IT & Cyber Security and Cloud of IT & Internet of Things
    IT & Business: Je leert hoe je IT-skills inzet voor bedrijven: je ondersteunt hen met software op maat, werkt klantvriendelijk en optimaliseert bedrijfsprocessen. Je past de software voortdurend aan de veranderende noden van de bedrijfswereld aan. Bijvoorbeeld: jij automatiseert het verzendproces van een voedingsbedrijf, waardoor verse producten nóg sneller in de rekken liggen. #businessapplications #web #sap #analysis #businessprocesses #bigdata #management
    IT & Artificial Intelligence: In het traject IT & Artificial Intelligence (AI) leer je om aan de slag te gaan met data en slimme toepassingen te maken die het dagelijks leven van iedereen verbeteren. Je ontdekt hoe je automatisch patronen kan vinden in data en je leert AI-software te ontwikkelen die bedrijven en de maatschappij een boost geven. 
    IT & Software: In het traject IT & Software werk je IT-oplossingen uit op maat van de klant. Door je technische skills te combineren met je analytische vaardigheden, ben je in staat om uitdagende softwareprojecten uit te werken. Zo leer je onder meer kwalitatieve code te schrijven en tegelijkertijd scherpen we je creativiteit en professionele vaardigheden aan. #software #mobile #web #fullstack #softwareengineering #programming
    IT & Cyber Security and Cloud: Je leert bedrijven te beschermen tegen cyberaanvallen, ransomware en datalekken. Snel veranderende technologieën zoals Internet of Things, machine learning, robotisering vragen om specialisten die zorgen voor een veilige IT-omgeving. Je ontdekt hoe je bedrijven kan ondersteunen in de transitie naar de cloud en hoe je complexe server/netwerk-combinaties kan automatiseren en beheren. #cybersecurity #systems #cloud #devops #networkspecialist
    IT & Internet of Things: Je leert IoT-systemen te ontwerpen en ontwikkelen. Je maakt de koppeling tussen hard- en software, waardoor je kan meebouwen aan de IoT-netwerken van de toekomst. Je ontdekt hoe je software kan ontwikkelen voor geconnecteerde devices (robots, drones, camera’s, grasmaaiers …) of hoe je slimme systemen kan ontwerpen voor de slimme steden van de toekomst.#embeddedprogramming #smarttech #prototyping #r&d #smartapplications #iotsystemen
    
    Onze praktijkgerichte graduaatsopleidingen van 120 studiepunten leiden je op programmeur, IoT-installateur of systeem- en netwerkbeheerder. In deze doe-opleidingen heb je meer praktijk dan theorie, en maak je al snel kennis met het werkveld dankzij het werkplekleren.
    Met je graduaatsdiploma ben je al meteen inzetbaar op de arbeidsmarkt. Maar uiteraard kan je ook verder studeren als je onze hypermoderne campus Spoor Noord nog niet wil verlaten.  Met een graduaatsdiploma in the pocket, kan je telkens met een vervolgtraject in no-time nog een bachelordiploma behalen.
    Al onze IT-graduaatsopleidingen kan je volgen in een dagtraject van twee jaar, of een avondtraject van drie (of vier) jaar. Op die manier is een (extra) graduaatsdiploma voor iedereen haalbaar, ook als je jouw opleiding wil combineren met een job of gezin.
    Graduaat Programmeren: We leiden je op tot een programmeur die de implementatie van softwareapplicaties tot een goed einde brengt. In deze doe-opleiding ga je al vanaf dag één aan de slag op onze moderne campus. Daarna sturen we je vroeg in het programma de werkvloer op. Onder begeleiding, en vaak in team, leer je programmeren en IT-projecten uitwerken. Je kan een rechtstreeks vervolgtraject volgen naar het bachelortraject IT & Software.#programming #web #cms #testing
    Graduaat Systeem- en Netwerkbeheer: We leiden je op tot een hands-on technicus die verantwoordelijk is voor de installatie, configuratie en het onderhoud van veilige digitale systemen en datacommunicatienetwerken. We zetten je onmiddellijk aan het werk in onze moderne labo’s. Je leert computernetwerken en de daaraan gekoppelde systemen implementeren en troubleshooten. Je kan een rechtstreeks vervolgtraject volgen naar het bachelortraject IT & Cyber Security and Cloud. #virtualisation #networking #system #servers #systemmanagement
    Graduaat Internet of Things: We leiden je op tot een hands-on technicus Internet of Things (IoT). Er is een grote nood aan gekwalificeerde techniekers die slimme toestellen correct kunnen configureren, installeren en optimaliseren, verbinden met het correcte netwerk en integreren in slimme gebouwen (domotica), bedrijven en industrieën. In deze doe-opleiding word jij hiervoor klaargestoomd. Je kan een rechtstreeks vervolgtraject volgen naar het bachelortraject IT & Internet of Things.#iot-installatie #lowpower #domotica #scripting #electric #networking
    
    Wil jij een goede basis leggen om websites te leren bouwen, maar heb je geen zin om een volledige graduaatsopleiding te volgen? Dan bieden we je de optie om je in te schrijven voor het micro degree Webontwikkeling, een traject met afstandsonderwijs dat je toelaat om je werk en studies met elkaar te combineren.
    Je studeert dus waar en wanneer je wil, en werkt onder begeleiding enkele realistische projecten uit verdeeld over twee modules. Er zijn tussentijds optionele contactmomenten op de campus en de evaluatie van elke eindopdracht vindt ook plaats on campus. Na afloop van een module krijg je een certificaat overhandigd.
    """

st.title("IT@AP Bot")
st.markdown("**Opgelet**: Stel gerust je vragen maar we kunnen de nauwkeurigheid en volledigheid van de antwoorden niet garanderen. Voor verdere vragen kan je altijd terecht bij de IT lectoren of op het mailadres bachelor.it@ap.be.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Ik ben een IT student aan de AP Hogeschool in Antwerpen. Hoe kan ik je helpen?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hoe kan ik je helpen?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #response = st.write_stream(response_generator())
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "system", "content": st.session_state.system_prompt}] +
            [{"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
        #print(stream.choices[0].message.content)
    # TTS
        # speech = client.audio.speech.create(
        #     model="tts-1",
        #     voice="nova",
        #     input=response)
        # file_path = os.getcwd() +"\\soundfile.mp3"
        # speech.stream_to_file(file_path)
        # audio_data, sample_rate = sf.read(file_path)
        # sd.play(audio_data, sample_rate)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



# if text := speech_to_text(
#     language='nl',
#     start_prompt="Opname",
#     stop_prompt="Stop opname",
#     use_container_width=False,just_once=True,key='STT'):
#     with st.chat_message("user"):
#         st.markdown(text)
#     st.session_state.messages.append({"role": "user", "content": text})
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         #response = st.write_stream(response_generator())
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[{"role": "system", "content": st.session_state.system_prompt}] +
#             [{"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#         #print(stream.choices[0].message.content)
#     # TTS
#         speech = client.audio.speech.create(
#             model="tts-1",
#             voice="nova",
#             input=response)
#         file_path = os.getcwd() +"\\soundfile.mp3"
#         speech.stream_to_file(file_path)
#         audio_data, sample_rate = sf.read(file_path)
#         sd.play(audio_data, sample_rate)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})


