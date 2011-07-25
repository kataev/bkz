dojo.provide('whs.parseInt');

whs.parseInt = function(val) {
                var total_int = '';
                var s = val.split(',');
                var len = s.length;
                for (var i = 0; i < len; i++) {
                    total_int += s[i];
                }
                return parseInt(total_int);
            }