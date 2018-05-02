config {
    set tmsa.configuration.confidence_threshold low
    set tmsa.decision_engine.html_js_use_yara 1
    set tmsa.decision_engine.swf_use_yara 1
    set tmsa.decision_engine.pdf_use_yara 1
    set tmsa.decision_engine.java_use_yara 1
    set tmsa.level.dynamicscript_detect 1
    set tmsa.level.feedback 1
    set tmsa.level.chain_analyzer 1
    set tmsa.level.phishing_detect 1
    set tmsa.phishing.block 0
    set tmsa.phishing.feedback 1
    set tmsa.log.level info
    set tmsa.nsc_traffic.enable 0
    set tmsa.nsc_cache.enable 0
    set tmsa.pdf_swf_engine.pdf_enable 1
    set tmsa.pdf_swf_engine.pdf_timeout 10000
    set tmsa.pdf_swf_engine.use_js_xfa_parser 1
    set tmsa.pdf_swf_engine.swf_enable 1
    set tmsa.pdf_swf_engine.swf_timeout 10000
    set tmsa.pdf_swf_engine.swf_shumway_solution 1
    set tmsa.pdf_swf_engine.breakout 1
    set tmsa.shellcode_engine.enable 0
    set tmsa.java_engine.enable 1
    set tmsa.java_engine.timeout 6000
    set tmsa.sie.enable 0
    set tmsa.sie.sie_only 0
    set tmsa.network_dynamic.enable 0
    set tmsa.endpoint_capture.enable 0
    set tmsa.endpoint_capture.feedback_prev_capture 0
    set tmsa.endpoint_capture.feedback_post_capture 0
}
