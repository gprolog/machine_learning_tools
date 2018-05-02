/*
===============================================================================
value in `meta` section:
  decision = "[malicious|suspicious|monitoring|normal]"
  confidence_level = "[high|medium|low]"
===============================================================================
*/

/*
===============================================================================
normal rules
===============================================================================
*/

// NOTE: add 'is_html_file' before enable this rule
rule no_script : generic
{
    meta:
        description = "No script in content"
        decision = "normal"
        confidence_level = "medium"
    strings:
        $a = "<script" nocase
    condition:
        is_html_file and (not $a) 
}

/*
===============================================================================
detection rules
===============================================================================
*/
/*
private rules
*/

rule cve_2014_6332 : specific
{
    meta:
        description = "CVE-2014-6332"
        decision = "malicious"
        confidence_level = "medium"
    strings:
        $s = "on error resume next" nocase
        $r = /\w{1,20}\s*=\s*\w{1,20}\s*\+\s*&h8000000[\w\W]{1,300}redim[\w\W]{1,300}redim[\w\W]{1,300}redim\s*preserve\s*\w{1,20}\s*\(s*\w{1,20}\s*\)/ nocase
    condition:
        $s and $r
}

rule cve_2014_6332_a : specific
{
	meta:
        description = "CVE-2014-6332"
        decision = "malicious"
        confidence_level = "medium"	  
	strings:
	  $s1 = "on error resume next" nocase
	  $r1 = /\sDim\s/ nocase
	  $r2 = /redim\s*preserve/ nocase
	  
	condition:
	  #s1 > 1 and #r1 > 1 and #r2 > 5
}

rule JS_VBS_CVE_2016_0189_A_exploit_encode : generic
{
    meta:
	author = "graysen_tong"
	description = "translate from salineup rule encoded by char to num"
	decision = "malicious"
	confidence_level = "medium"
	sha1 = "fca44a44bb0cbe0082a38bef235bc2e5a51417c0"

    strings:
	$s1 = "67,83,110,103"  /* match keyword  "CSng" */
	$s2 = "86,97,114,84,121,112,101" /* match keyword  "VarType" */
	$s3 = "67,108,97,115,115,95,73,110,105,116,105,97,108,105,122,101" /* match keyword  "Class_Initialize" */
	$s4 = "82,101,68,105,109"  /* match "Redim" keyword */
	$s5 = "38,72,49,55,52" /* match keyword  "&H134" */
	$s6 = "38,72,49,51,56" /* match keyword  "&H138" */
	$s7 = "38,72,49,54,56" /* match keyword  "&H168" */
	$s8 = "38,72,49,51,52" /* match keyword  "&H174" */

    condition:
	$s1 and $s2 and $s3 and $s4 and ($s5 or $s6 or $s7 or $s8)
}

rule JS_VBS_CVE_2016_0189_A_valueof_encode : generic
{
    meta:
	author = "graysen_tong"
	description = "translate from salineup rule encoded by char to num"
	decision = "malicious"
	confidence_level = "medium"
	sha1 = "e46aab1ba26400208b0ab69cccb5f9e4ea6c8e1d"

   strings:
	$s1 = "118,97,108,117,101,79,102" /* match keyword  "valueOf" */
	$s2 = "102,117,110,99,116,105,111,110" /* match keyword  "function" */

   condition:
	$s1 and $s2
}

rule JS_VBS_CVE_2016_0189_A : generic
{
    meta:
	author = "hongying_yu"
	description = "translate from salineup rule encoded by char to num"
	decision = "malicious"
	confidence_level = "medium"
	sha1 = "e46aab1ba26400208b0ab69cccb5f9e4ea6c8e1d"

   strings:
   	$s0 = "vbscript" nocase
	$s1 = "CSng" nocase
	$s2 = "VarType" nocase
	$s3 = "Class_Initialize" nocase
	$r1 = /ReDim\s+Preserve\s+\w{1,10}\s?\(1\s?,\s?1\s?\)/ nocase
   condition:
		all of them
}

rule cve_2013_3897 : specific
{
    meta:
        description = "CVE-2013-3897"
        decision = "malicious"
        confidence_level = "medium"
    strings:
        $s1 = ".swapnode" nocase
        $s2 = ".onselect" nocase
        $s3 = ".execcommand" nocase
        $s4 = ".onpropertychange" nocase
        $r = /unescape\s*\(\s*['"](%u4141%u4141|%u1414%u1414)/ nocase
    condition:
        all of them
}

rule JS_RISKACX_C_encode : generic
{
    meta:
	author = "graysen_tong"
	description = "translate from salineup rule encoded by char to num"
	decision = "malicious"
	confidence_level = "medium"
	sha1 = "a2bca14a4ee78b1aa67a3d1a9825001eb9b29834"

   strings:
	$s1 = "83,97,118,101,84,111,70,105,108,101" /* match "SaveToFile" keyword */
	$s2 = "83,104,101,108,108,69,120,101,99,117,116,101" /* match "ShellExecute" keyword */
	$s3 = "114,117,110" /* match "run" keyword */

   condition:
	$s1 and ($s2 or $s3)
}

rule JS_payload_A : specific
{
    meta:
	author = "hongying_yu"
	description = "for payload_1"
	decision = "malicious"
	confidence_level = "medium"
	sha1 = "653c35bbbed6642089939be721f18936de8b7aa1"

   strings:
	$s1 = "payload_1"
	$s2 = "payload_2"
	$s3 = "base64DecodeChars"
	$s4 = "base64decode"

   condition:
	$s1 and $s2 and $s3 and $s4
}

rule JS_jscript_encoder_A:specific

{

    meta:

	author = "hongying_yu"

	description = "for jscript encoder"

	decision = "malicious"

	confidence_level = "medium"

	sha1 = "da17977843b5d80921b0c306db331dca559b2754"

   strings:

	$s1 = "VBScript.Encode"
	$s2 = "JScript.Encode"
	$s3 = ""
	$s4 = "@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$"

   condition:

	$s1 and $s2 and $s3 and $s4

}