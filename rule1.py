import tamil

def vallinam_mighuthal_checker(nilaimozhi, varumozhi, punarnthamozhi):
    """
    அல்வழியில் அகர ஈற்றுப் பெயர்ச்சொல்லின் முன் வரும் வல்லினம் மிகுதலைச் 
    சரிபார்க்கும் பொதுவான பயன்பாட்டுச் சார்பு (Utility Function).

        Parameters:
            nilaimozhi (str)   : நிலைமொழி (எ-டு: 'விள')
            varumozhi (str)    : வருமொழி (எ-டு: 'கடிது')
            punarnthamozhi (str): புணர்ந்த புதிய மொழி (எ-டு: 'விளக்கடிது')

        Returns:
            result (bool):
                True  - விதிமுறைப்படி வல்லினம் சரியாக மிகுந்து வந்துள்ளது.
                False - வல்லினம் மிகவில்லை அல்லது தவறான எழுத்து மிகுந்துள்ளது.
    """
    # 1. நிலைமொழியின் இறுதி எழுத்தைப் பிரித்தல்
    nilai_letters = tamil.utf8.get_letters(nilaimozhi)
    if not nilai_letters:
        return False
    nilai_eiru = nilai_letters[-1] # நிலைமொழியின் கடைசி எழுத்து
    
    # உயிர்மெய்யைப் பிரித்து அகர ஈறா எனச் சரிபார்த்தல் (எ-டு: ள = ள் + அ)
    nilai_split = tamil.utf8.splitMeiUyir(nilai_eiru)
    if type(nilai_split) is tuple:
        uyir_eiru = nilai_split[1] # உயிர் ஈறு மட்டும்
    else:
        uyir_eiru = nilai_split     # தனி உயிரெழுத்தாக இருந்தால் (அ)
        
    # 2. வருமொழியின் முதல் எழுத்தின் மெய்யைப் பிரித்தல் (வல்லினமா என அறிய)
    varu_letters = tamil.utf8.get_letters(varumozhi)
    if not varu_letters:
        return False
    varu_muthal = varu_letters[0]
    
    varu_split = tamil.utf8.splitMeiUyir(varu_muthal)
    if type(varu_split) is tuple:
        varu_mei_muthal = varu_split[0] # வருமொழி முதலின் மெய்யெழுத்து (க், ச், த், ப்)
    else:
        varu_mei_muthal = None # உயிரெழுத்தாக இருந்தால் வல்லினம் இல்லை

    vallinam = ["க்", "ச்", "த்", "ப்"]

    # நிபந்தனை: அகர ஈறாக இருந்து, வருமொழி முதலில் வல்லினம் இருந்தால் மட்டுமே விதி பொருந்தும்
    if uyir_eiru == "அ" and varu_mei_muthal in vallinam:
        # எதிர்பாக்கும் சரியான புணர்ச்சி வடிவம் (நிலைமொழி + மிகு மெய் + வருமொழி)
        expected_word = nilaimozhi + varu_mei_muthal + varumozhi
        
        if punarnthamozhi == expected_word:
            return True
        else:
            return False
            
    return None # அகர ஈறு அல்லது வருமொழி வல்லினம் இல்லையெனில் விதிக்கு அப்பாற்பட்டது


# "புணர்ச்சி_விதி_1": அகர ஈற்றுப் பெயர் + க,ச,த,ப (அல்வழி) -> வல்லினம் மிகுதல்
def sandhi_agara_eiru_alvazhi(nilaimozhi, varumozhi, punarnthamozhi):
    """
    தொல்காப்பிய புணரியல் விதிப்படி, அல்வழிப் புணர்ச்சியில் அகர ஈற்றுப் 
    பெயர்ச்சொற்களின் பின் வரும் வல்லினம் (க, ச, த, ப) மிகும் விதியின் செயலாக்கம்.

    எடுத்துக்காட்டு:
        விள + கடிது = விளக்கடிது (சரி - True)
        விள + கடிது = விளகடிது  (தவறு - False)

        Parameters:
            nilaimozhi (str)   : நிலைமொழி
            varumozhi (str)    : வருமொழி
            punarnthamozhi (str): சரிபார்க்க வேண்டிய புணர்ந்த சொல்

        Returns:
            result (bool):
                True  - விதி பொருந்தி, இலக்கணப்படி சரியாக உள்ளது.
                False - விதி பொருந்தி, ஆனால் இலக்கணப் பிழையாக உள்ளது.
                None  - அகர ஈறோ அல்லது வருமொழி முதல் வல்லினமோ இல்லை (விதி பொருந்தாது).
    """
    # பொதுச் சார்பை அழைத்து முடிவை அறிதல்
    return vallinam_mighuthal_checker(nilaimozhi, varumozhi, punarnthamozhi)