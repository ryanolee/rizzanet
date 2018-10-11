vcl 4.1;



backend rizzanet{
    .host =  "${VARNISH_BACKEND_HOST}";
    .port = "${VARNISH_BACKEND_PORT}";
    .max_connections = ${VARNISH_BACKEND_MAX_CONNECTIONS};
}

acl ban_ips{
    "127.0.0.1";
    "web";
}

sub vcl_backend_fetch{
    set bereq.http.X-rizzanet-varnish = "${VARNSIH_BACKEND_HEADER_VALUE}";
    return(fetch);
}

sub vcl_backend_response {
    set beresp.do_gzip = true;
    set beresp.grace = 5d;
    set beresp.keep = 5d;
    unset beresp.http.X-rizzanet-ban-tags;
    return(deliver);
}

sub vcl_recv{
    if (req.method == "BAN") {
        if( client.ip !~ ban_ips){
            return(synth(405, "Forbidden"));
        }
        if( req.http.X-rizzanet-ban-tags != ""){
            ban( "obj.http.X-rizzanet-ban-tags ~ " + req.http.X-rizzanet-ban-tags);
            return(synth(200, "Banned"));
        }
        return(synth(304, ""));
    }
    return(hash);
}
