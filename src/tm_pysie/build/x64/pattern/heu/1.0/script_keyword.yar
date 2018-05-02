
rule keyword_return{
    meta:
        index="0"
        TFIDF="0.0324931740329"
    strings:
        $s="return" fullword nocase
    condition:
        $s
    }

 
rule keyword_function{
    meta:
        index="1"
        TFIDF="0.0316148844365"
    strings:
        $s="function" fullword nocase
    condition:
        $s
    }

 
rule keyword_ndefi{
    meta:
        index="2"
        TFIDF="0.00121058968741"
    strings:
        $s="ndefi" fullword nocase
    condition:
        $s
    }

 
rule keyword_height{
    meta:
        index="3"
        TFIDF="0.0369642089353"
    strings:
        $s="height" fullword nocase
    condition:
        $s
    }

 
rule keyword_left{
    meta:
        index="4"
        TFIDF="0.034126740116"
    strings:
        $s="left" fullword nocase
    condition:
        $s
    }

 
rule keyword_width{
    meta:
        index="5"
        TFIDF="0.0362844153018"
    strings:
        $s="width" fullword nocase
    condition:
        $s
    }

 
rule keyword_else{
    meta:
        index="6"
        TFIDF="0.0142651510226"
    strings:
        $s="else" fullword nocase
    condition:
        $s
    }

 
rule keyword_regexp{
    meta:
        index="7"
        TFIDF="0.0137813939894"
    strings:
        $s="regexp" fullword nocase
    condition:
        $s
    }

 
rule keyword_style{
    meta:
        index="8"
        TFIDF="0.0768332464768"
    strings:
        $s="style" fullword nocase
    condition:
        $s
    }

 
rule keyword_jquery{
    meta:
        index="9"
        TFIDF="0.161518139203"
    strings:
        $s="jquery" fullword nocase
    condition:
        $s
    }

 
rule keyword_gfgf{
    meta:
        index="10"
        TFIDF="0.00242117937483"
    strings:
        $s="gfgf" fullword nocase
    condition:
        $s
    }

 
rule keyword_typeof{
    meta:
        index="11"
        TFIDF="0.0319774081208"
    strings:
        $s="typeof" fullword nocase
    condition:
        $s
    }

 
rule keyword_document{
    meta:
        index="12"
        TFIDF="0.0592014179875"
    strings:
        $s="document" fullword nocase
    condition:
        $s
    }

 
rule keyword_license{
    meta:
        index="13"
        TFIDF="0.0213088751213"
    strings:
        $s="license" fullword nocase
    condition:
        $s
    }

 
rule keyword_value{
    meta:
        index="14"
        TFIDF="0.096734749712"
    strings:
        $s="value" fullword nocase
    condition:
        $s
    }

 
rule keyword_with{
    meta:
        index="15"
        TFIDF="0.0381331283897"
    strings:
        $s="with" fullword nocase
    condition:
        $s
    }

 
rule keyword_swqfa{
    meta:
        index="16"
        TFIDF="0.00121671742389"
    strings:
        $s="swqfa" fullword nocase
    condition:
        $s
    }

 
rule keyword_split{
    meta:
        index="17"
        TFIDF="0.00923201941487"
    strings:
        $s="split" fullword nocase
    condition:
        $s
    }

 
rule keyword_unescape{
    meta:
        index="18"
        TFIDF="0.0539467615575"
    strings:
        $s="unescape" fullword nocase
    condition:
        $s
    }

 
rule keyword_hidden{
    meta:
        index="19"
        TFIDF="0.036398919732"
    strings:
        $s="hidden" fullword nocase
    condition:
        $s
    }

 
rule keyword_window{
    meta:
        index="20"
        TFIDF="0.0941665980316"
    strings:
        $s="window" fullword nocase
    condition:
        $s
    }

 
rule keyword_each{
    meta:
        index="21"
        TFIDF="0.0504093954144"
    strings:
        $s="each" fullword nocase
    condition:
        $s
    }

 
rule keyword_http{
    meta:
        index="22"
        TFIDF="0.0176746032157"
    strings:
        $s="http" fullword nocase
    condition:
        $s
    }

 
rule keyword_parent{
    meta:
        index="23"
        TFIDF="0.104930980504"
    strings:
        $s="parent" fullword nocase
    condition:
        $s
    }

 
rule keyword_length{
    meta:
        index="24"
        TFIDF="0.0146405918314"
    strings:
        $s="length" fullword nocase
    condition:
        $s
    }

 
rule keyword_arguments{
    meta:
        index="25"
        TFIDF="0.0538235031041"
    strings:
        $s="arguments" fullword nocase
    condition:
        $s
    }

 
rule keyword_getelementbyid{
    meta:
        index="26"
        TFIDF="0.0373805218688"
    strings:
        $s="getelementbyid" fullword nocase
    condition:
        $s
    }

 
rule keyword_html{
    meta:
        index="27"
        TFIDF="0.0552930361651"
    strings:
        $s="html" fullword nocase
    condition:
        $s
    }

 
rule keyword_createobject{
    meta:
        index="28"
        TFIDF="0.00720514199027"
    strings:
        $s="createobject" fullword nocase
    condition:
        $s
    }

 
rule keyword_string{
    meta:
        index="29"
        TFIDF="0.166962103462"
    strings:
        $s="string" fullword nocase
    condition:
        $s
    }

 
rule keyword_none{
    meta:
        index="30"
        TFIDF="0.0262279073478"
    strings:
        $s="none" fullword nocase
    condition:
        $s
    }

 
rule keyword_false{
    meta:
        index="31"
        TFIDF="0.0212371549859"
    strings:
        $s="false" fullword nocase
    condition:
        $s
    }

 
rule keyword_show{
    meta:
        index="32"
        TFIDF="0.0370426053454"
    strings:
        $s="show" fullword nocase
    condition:
        $s
    }

 
rule keyword_event{
    meta:
        index="33"
        TFIDF="0.104523930998"
    strings:
        $s="event" fullword nocase
    condition:
        $s
    }

 
rule keyword_title{
    meta:
        index="34"
        TFIDF="0.0765237767326"
    strings:
        $s="title" fullword nocase
    condition:
        $s
    }

 
rule keyword_true{
    meta:
        index="35"
        TFIDF="0.0141211594403"
    strings:
        $s="true" fullword nocase
    condition:
        $s
    }

 
rule keyword_parseint{
    meta:
        index="36"
        TFIDF="0.0266667951517"
    strings:
        $s="parseint" fullword nocase
    condition:
        $s
    }

 
rule keyword_content{
    meta:
        index="37"
        TFIDF="0.338660438063"
    strings:
        $s="content" fullword nocase
    condition:
        $s
    }

 
rule keyword_display{
    meta:
        index="38"
        TFIDF="0.0413625429531"
    strings:
        $s="display" fullword nocase
    condition:
        $s
    }

 
rule keyword_math{
    meta:
        index="39"
        TFIDF="0.109061792099"
    strings:
        $s="math" fullword nocase
    condition:
        $s
    }

 
rule keyword_hide{
    meta:
        index="40"
        TFIDF="0.050993037439"
    strings:
        $s="hide" fullword nocase
    condition:
        $s
    }

 
rule keyword_extend{
    meta:
        index="41"
        TFIDF="0.0165076018062"
    strings:
        $s="extend" fullword nocase
    condition:
        $s
    }

 
rule keyword_options{
    meta:
        index="42"
        TFIDF="0.149167599235"
    strings:
        $s="options" fullword nocase
    condition:
        $s
    }

 
rule keyword_name{
    meta:
        index="43"
        TFIDF="0.0474865427634"
    strings:
        $s="name" fullword nocase
    condition:
        $s
    }

 
rule keyword_indexof{
    meta:
        index="44"
        TFIDF="0.0280672527149"
    strings:
        $s="indexof" fullword nocase
    condition:
        $s
    }

 
rule keyword_chrw{
    meta:
        index="45"
        TFIDF="0.0315316122837"
    strings:
        $s="chrw" fullword nocase
    condition:
        $s
    }

 
rule keyword_under{
    meta:
        index="46"
        TFIDF="0.0088170334737"
    strings:
        $s="under" fullword nocase
    condition:
        $s
    }

 
rule keyword_funclass{
    meta:
        index="47"
        TFIDF="0.00266661840461"
    strings:
        $s="funclass" fullword nocase
    condition:
        $s
    }

 
rule keyword_redim{
    meta:
        index="48"
        TFIDF="0.0312222819577"
    strings:
        $s="redim" fullword nocase
    condition:
        $s
    }

 
rule keyword_null{
    meta:
        index="49"
        TFIDF="0.0285185028951"
    strings:
        $s="null" fullword nocase
    condition:
        $s
    }

 
rule keyword_position{
    meta:
        index="50"
        TFIDF="0.0537889790965"
    strings:
        $s="position" fullword nocase
    condition:
        $s
    }

 
rule keyword_array{
    meta:
        index="51"
        TFIDF="0.035639184977"
    strings:
        $s="array" fullword nocase
    condition:
        $s
    }

 
rule keyword_write{
    meta:
        index="52"
        TFIDF="0.12091843714"
    strings:
        $s="write" fullword nocase
    condition:
        $s
    }

 
rule keyword_data{
    meta:
        index="53"
        TFIDF="0.106804765293"
    strings:
        $s="data" fullword nocase
    condition:
        $s
    }

 
rule keyword_copyright{
    meta:
        index="54"
        TFIDF="0.0214276188658"
    strings:
        $s="copyright" fullword nocase
    condition:
        $s
    }

 
rule keyword_licenses{
    meta:
        index="55"
        TFIDF="0.0257210459289"
    strings:
        $s="licenses" fullword nocase
    condition:
        $s
    }

 
rule keyword_undefined{
    meta:
        index="56"
        TFIDF="0.0784061019445"
    strings:
        $s="undefined" fullword nocase
    condition:
        $s
    }

 
rule keyword_remove{
    meta:
        index="57"
        TFIDF="0.020983360454"
    strings:
        $s="remove" fullword nocase
    condition:
        $s
    }

 
rule keyword_wscript{
    meta:
        index="58"
        TFIDF="0.00493339622087"
    strings:
        $s="wscript" fullword nocase
    condition:
        $s
    }

 
rule keyword_class{
    meta:
        index="59"
        TFIDF="0.0254557090211"
    strings:
        $s="class" fullword nocase
    condition:
        $s
    }

 
rule keyword_lenb{
    meta:
        index="60"
        TFIDF="0.00248352448897"
    strings:
        $s="lenb" fullword nocase
    condition:
        $s
    }

 
rule keyword_object{
    meta:
        index="61"
        TFIDF="0.0291534204423"
    strings:
        $s="object" fullword nocase
    condition:
        $s
    }

 
rule keyword_xpost{
    meta:
        index="62"
        TFIDF="0.0108277879671"
    strings:
        $s="xpost" fullword nocase
    condition:
        $s
    }

 
rule keyword_version{
    meta:
        index="63"
        TFIDF="0.0365961146462"
    strings:
        $s="version" fullword nocase
    condition:
        $s
    }

 
rule keyword_current{
    meta:
        index="64"
        TFIDF="0.0646913881928"
    strings:
        $s="current" fullword nocase
    condition:
        $s
    }

 
rule keyword_javascript{
    meta:
        index="65"
        TFIDF="0.0339747837949"
    strings:
        $s="javascript" fullword nocase
    condition:
        $s
    }

 
rule keyword_objwsh{
    meta:
        index="66"
        TFIDF="0.0108277879671"
    strings:
        $s="objwsh" fullword nocase
    condition:
        $s
    }

 
rule keyword_span{
    meta:
        index="67"
        TFIDF="0.105978471251"
    strings:
        $s="span" fullword nocase
    condition:
        $s
    }

 
rule keyword_init{
    meta:
        index="68"
        TFIDF="0.0402625389106"
    strings:
        $s="init" fullword nocase
    condition:
        $s
    }

 
rule keyword_link{
    meta:
        index="69"
        TFIDF="0.157229257393"
    strings:
        $s="link" fullword nocase
    condition:
        $s
    }

 
rule keyword_first{
    meta:
        index="70"
        TFIDF="0.035403182263"
    strings:
        $s="first" fullword nocase
    condition:
        $s
    }

 
rule keyword_vartype{
    meta:
        index="71"
        TFIDF="0.0120085699838"
    strings:
        $s="vartype" fullword nocase
    condition:
        $s
    }

 
rule keyword_body{
    meta:
        index="72"
        TFIDF="0.0417779916171"
    strings:
        $s="body" fullword nocase
    condition:
        $s
    }

 
rule keyword_absolute{
    meta:
        index="73"
        TFIDF="0.0327013409672"
    strings:
        $s="absolute" fullword nocase
    condition:
        $s
    }

 
rule keyword_fromcharcode{
    meta:
        index="74"
        TFIDF="0.0473958422648"
    strings:
        $s="fromcharcode" fullword nocase
    condition:
        $s
    }

 
rule keyword_testaa{
    meta:
        index="75"
        TFIDF="0.00533323680922"
    strings:
        $s="testaa" fullword nocase
    condition:
        $s
    }

 
rule keyword_find{
    meta:
        index="76"
        TFIDF="0.0543929860563"
    strings:
        $s="find" fullword nocase
    condition:
        $s
    }

 
rule keyword_right{
    meta:
        index="77"
        TFIDF="0.0265445315962"
    strings:
        $s="right" fullword nocase
    condition:
        $s
    }

 
rule keyword_target{
    meta:
        index="78"
        TFIDF="0.14111407723"
    strings:
        $s="target" fullword nocase
    condition:
        $s
    }

 
rule keyword_resume{
    meta:
        index="79"
        TFIDF="0.0162767817762"
    strings:
        $s="resume" fullword nocase
    condition:
        $s
    }

 
rule keyword_addclass{
    meta:
        index="80"
        TFIDF="0.0616678234645"
    strings:
        $s="addclass" fullword nocase
    condition:
        $s
    }

 
rule keyword_image{
    meta:
        index="81"
        TFIDF="0.0453045606622"
    strings:
        $s="image" fullword nocase
    condition:
        $s
    }

 
rule keyword_index{
    meta:
        index="82"
        TFIDF="0.0650265851981"
    strings:
        $s="index" fullword nocase
    condition:
        $s
    }

 
rule keyword_push{
    meta:
        index="83"
        TFIDF="0.0328511162739"
    strings:
        $s="push" fullword nocase
    condition:
        $s
    }

 
rule keyword_href{
    meta:
        index="84"
        TFIDF="0.0718816357019"
    strings:
        $s="href" fullword nocase
    condition:
        $s
    }

 
rule keyword_bind{
    meta:
        index="85"
        TFIDF="0.0247432625012"
    strings:
        $s="bind" fullword nocase
    condition:
        $s
    }

 
rule keyword_preserve{
    meta:
        index="86"
        TFIDF="0.0240171399675"
    strings:
        $s="preserve" fullword nocase
    condition:
        $s
    }

 
rule keyword_images{
    meta:
        index="87"
        TFIDF="0.0198869964306"
    strings:
        $s="images" fullword nocase
    condition:
        $s
    }

 
rule keyword_block{
    meta:
        index="88"
        TFIDF="0.0204374150063"
    strings:
        $s="block" fullword nocase
    condition:
        $s
    }

 
rule keyword_offsetheight{
    meta:
        index="89"
        TFIDF="0.0286480128875"
    strings:
        $s="offsetheight" fullword nocase
    condition:
        $s
    }

 
rule keyword_this{
    meta:
        index="90"
        TFIDF="0.0483084973247"
    strings:
        $s="this" fullword nocase
    condition:
        $s
    }
