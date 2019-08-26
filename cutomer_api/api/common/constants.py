import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_TYPE = {
	0 : 'email',
	1 : 'phone'
}

USER_ROLE = (
				(0,'Admin'),
				(1,'Sales'),
				(2,'Lsp'),
				(3,'Normal')
			)

GENDER_TYPE = (
					(0,"female"),
					(1,"male"),
					(2,"others")
			  )
PROFILE_TYPE = (
					(0,"self"),
					(1,"siblings")
				)
TIME_FRAME = (
				(0,"seconds"),
				(1,"minutes"),
				(2,"hours")
			)
ACCOUNT_TYPE = (
					(0,"HOME"),
					(1,"OFFICE"),
					(2,"OTHERS")
				)

COOKIE_TYPE =  (
					(0,"SESSION"),
					(1,"PERSISTANCE")
				)
COOKIE_SHARED_TYPE =  (
						(0,"INDIVIDUAL"),
						(1,"SHARED")
					)
COOKIE_STORAGE_ENGINE = (
							(0,"REDIS"),
							(1,"MEMCACHE")
						)			
MIMETYPE = {
	"xml" : "text/xml",
	"json" : "application/json",
	"html" : "text/html"
}

NOTIFICATION = [0,1]

EMAIL_TEMPLATE = {
	"1" : {
		"title": "OTP Generated",
		"subject" : "Hi, your OTP Generated",
		"template_path" : '/home/saurabh/workplace/customer_api/api/static/change_password.html'

		},
	"2" : {
		"title": "Account Created",
		"subject" : "Hi, your Account is created",
		"template_path" : '/home/saurabh/workplace/customer_api/api/static/change_password.html'

		},
	"3" : {
		"title": "Change Password",
		"subject" : "Hi, your Password is changed",
		"template_path" : '/home/saurabh/workplace/customer_api/api/static/change_password.html'

		},
	"4" : {
		"title": "Forget Password",
		"subject" : "Hi, your Reset password link :",
		"template_path" : '/home/saurabh/workplace/customer-api/api/static/forgot.html'

		},

}

SMS_TEMPLATE = {
	"1" : {
		"message" : "To Change your password,Please insert this OTP #OTPVALUE"
	}
}


response_codes = {
	"100" : "continue",
	"101" : "switching protocols",
	"102" : "processing",
	"200" : "ok",
	"201" : "created",
	"202" : "accepted",
	"203" : "non-authoritative information",
	"204" : "no content",
	"205" : "reset content",
	"206" : "partial content",
	"207" : "multi-status",
	"208" : "already reported",
	"226" : "im used",
	"300" : "multiple choices",
	"301" : "moved permanently",
	"302" : "found",
	"303" : "see other",
	"304" : "not modified",
	"305" : "use proxy",
	"307" : "temporary redirect",
	"308" : "permanent redirect",
	"400" : "bad request",
	"401" : "unauthorized",
	"402" : "payment required",
	"403" : "forbidden",
	"404" : "not found",
	"405" : "method not allowed",
	"406" : "not acceptable",
	"407" : "proxy authentication required",
	"408" : "request timeout",
	"409" : "conflict",
	"410" : "gone",
	"411" : "length required",
	"412" : "precondition failed",
	"413" : "payload too large",
	"414" : "uri too long",
	"415" : "unsupported media type",
	"416" : "range not satisfiable",
	"417" : "expectation failed",
	"418" : "I'm a teapot",
	"422" : "unprocessable entity",
	"423" : "locked",
	"424" : "failed dependency",
	"426" : "upgrade required",
	"428" : "precondition required",
	"429" : "too many requests",
	"431" : "request header fields too large",
	"500" : "internal server error",
	"501" : "not implemented",
	"502" : "bad gateway",
	"503" : "service unavailable",
	"504" : "gateway timeout",
	"505" : "http version not supported",
	"506" : "variant also negotiates",
	"507" : "insufficient storage",
	"508" : "loop detected",
	"510" : "not extended",
	"511" : "network authentication required"
}
