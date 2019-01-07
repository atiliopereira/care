		function format(input){
			var vector = input.value.split(",");
			var num = vector[0].replace(/\./g,'');
			if(!isNaN(num)){
				num = num.toString().split('').reverse().join('').replace(/(?=\d*\.?)(\d{3})/g,'$1.');
				num = num.split('').reverse().join('').replace(/^[\.]/,'');
				if(vector.length>1){
					vector[1] = vector[1].replace('.','');
					if(!isNaN(vector[1])){
						input.value = num+","+ vector[1];
					}else{
						input.value = num+","+ vector[1].replace(/[^\d\.]*/g,'');
					}
				}else{
					input.value = num;	  
				}
			}
			  
			else{ //alert('Solo se permiten numeros');
				input.value = input.value.replace(/[^\d\.]*/g,'');
			}
		}

		function unformat(input){
			return input.value.replace(/\./g,'').replace(',','.');
		}

