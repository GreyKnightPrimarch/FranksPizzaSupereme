var Stotal = {"Crustout": .59, "Sizeout":1.0 };

        function getValueOfSize(input) {
            var val = input.value;
            val = GetJson(val);
            var input3 = document.getElementById('Sizeout');
            input3.value = val.Multiplier.toString();

            put(Stotal,'Sizeout', val.Multiplier )
            GetTotal()
        }

        function GetJson(val) {
            val = val.replace(/'/g, '"');
            var obj = JSON.parse(val);
            return obj;
        }

        Object.defineProperty(String.prototype, "GetJson", {
            value: function GetJson() {
                var val = this.replace(/'/g, '"');
                val = JSON.parse(val);
                return val;
            },
            writable: true,
            configurable: true,
        });

        function getValueOfCrust(input) {
            var dict = input.value;
            dict = GetJson(dict);
            var input3 = document.getElementById('Crustout');
            input3.value = dict.price.toString();

            put(Stotal,'Crustout', dict.price)
            GetTotal()
        }

        function round(value, decimals) {
            return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);

        }

        function put(object, key, value) {
            if (object === null || object === undefined) {
                object = {}
            }

            if (key in object) {
                object[key] = value;
            } else {
                object[key] = value;
            }
            return object;
        }

        function UpdateVal(val) {

            var id = val.id
            id = "S" + id
            var id2 = val.id
            id2 = "B" + id2
            var input1 = document.getElementById(id2);

            var bp = input1.innerText;
            bp = parseFloat(bp)
            var num = parseFloat(val.value)
            var result = round((num * bp), 2).toString();
            //load to global dictionary
            var global = put(window.Stotal, id, result)

            var input2 = document.getElementById(id);
            input2.innerText = result;
            //console.log(input1, result, num, bp, val.id, id);
            Stotal = global;
            GetTotal();
        }

        function GetTotal() {

            var a = Stotal;
            var keys = Object.keys(a);

            
            var len = keys.length;
            var temp1, temp2, sum;
            sum = temp1 = temp2 = 0;
            //console.log(a, keys);
            for (let index = 0; index < len; index++) {

                if (keys[index] == 'Crustout') {
                    temp1 = parseFloat(a[keys[index]])
                } else if (keys[index] == 'Sizeout') {
                    temp2 = parseFloat(a[keys[index]])
                } else {
                    sum += parseFloat(a[keys[index]])
                }

            }
            temp1 *= temp2;
            sum += temp1;
            sum = round(sum,2)
            //console.log(temp1, sum)
            var totf = document.getElementById('Total');
            totf.innerText = sum.toString();
        }