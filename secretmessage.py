# The following is an easter egg. As far as i know only fuzzy_factorp2_factorise(num) 
# can factor this number. Enjoy the message and ponder what it means. The security of
# using numbers like this are lacking to say the least, but it least we can factor it
# and enjoy an easter egg. It will take less than 2 minutes to factor, but only nano
# seconds once you find it's secret message about it's security.
# Run on the cmd line by: python3 secretmessage.py

from larsprime import *

e=65537

N=3176766231019168047779935388200097820433440940018864273811639933063724010036462572464536816452463822043693039747533696923500251937487517949404356825600544036344455908035583560540390217230299228602535954416742432484892734669356970162868285225878336857345442727250597155312251875886802639364567083582236778759931726123102495613076389466063225796848630163810544079872327896179184153761054749292796905880507931009486609892811110825603694618585322639248116766765050579745484946965056582381614029968601579847765230488964923950909898298615223650749825248644519257855795722324222242529216532996376765654365240895983915591402328878928179829509433301762871147151716050836002228490311121921123667331888118688678002861438592177959094450165484573531239048431688855058850149165667045024502706355401343523492300169525565942323739529466084179588588703120113346761416180101719517685091844916410227679233541787863602145894009128305792905271103077635689671065379632741846171490581261948511670236993033943675413602771776681340931257956645473223

cipher=1296828322437249144266196026720341038468269164865454727130052639848271621925980024126263011925286006483954387959158747590510150464903789919782168548783806524058850285984837484984619738860523888965558224300547679977582021458831831899131031654382108496575782126991641609335695208374354042293651760015956785074122496178558400700315415568184471811935031296453476448465919568941570867905175613322028287182636348493839905610239603357083583908675655085129053551884795316403656285617883092614678359116717453103612588581166841354066340422543802218988884663646987969130925585649214335287697434166697477608375212520912220378337867973031467866708920036280043611975115656062395994294214952835263268741883431820987740771791675168643860846874419025162103355200149588908926336354124488391590631588577588035743657053568679670512375627898372565836021945194591813870686478627167050182989450097687125142951557016199120368413665922583229258799279054827337076367472342940421900252542325899502577043435873620398076688026391601899118498149370268525

p,q = fuzzy_factorp2_factorise(N)

PHI=(p-1)*(q-1)

d=inv_mod(e,PHI)

message=pow(cipher,d,N)

print()
print()

print(bytes.fromhex(hex(int(str((abs(message))),10))[2:]))
