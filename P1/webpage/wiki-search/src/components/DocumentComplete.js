import React, { useEffect, useState } from "react";


export default function DocumentComplete() {
    const [array, setArray] = useState([]);
    function resaltarFrase(texto, frase) {
        try {
            const expresionRegular = new RegExp(frase, 'gi'); // Agregar 'i' para hacerlo no case-sensitive
    
            // Reemplazamos todas las ocurrencias de la frase con la frase rodeada por las etiquetas <mark>
            const textoResaltado = texto.replace(expresionRegular, "<mark>$&</mark>");
    
            return textoResaltado;
        } catch (err) {
            console.log(err);
            return texto;
        }
    }
    
    const apiUrl =
    "http://127.0.0.1:5000/document?titulo=" +
    search +
    "&tipoRecurso=" +
    tipoDB;

  //Realizar la solicitud POST
  axios
    .get(apiUrl)
    .then((response) => {
      if (response.status) {
        setArray(response.data[0]);
        
      } else {
        alert("holi 1");
      }
    })
    .catch((error) => {
      // Si ocurre un error en la solicitud
      console.log(error);
      console.error("Error en la solicitud:", error);
      //console.error('Error en la solicitud:', error);
      //console.error('Error en la solicitud:', error);
      
     
 
    });




useEffect(() => {
    try{
if (array.length > 0) {
    document.getElementById("contenido").innerHTML = resaltarFrase(,);
}} catch (error) {
      console.log(array[i])
      console.error(error)
    }
    
  
}, [array]);

    function wikiTextToHtml(wikiText) {
        // Encuentra y reemplaza las marcas de negrita ('''')
        wikiText = wikiText.replace(/'''(.*?)'''/g, '<strong>$1</strong>');

        // Encuentra y reemplaza las marcas de cursiva (''')
        wikiText = wikiText.replace(/''(.*?)''/g, '<em>$1</em>');

        // Encuentra y reemplaza los encabezados de nivel 5 (====== Título ======)
        wikiText = wikiText.replace(/======\s(.*?)\s======/g, '<h6>$1</h6>');

        // Encuentra y reemplaza los encabezados de nivel 4 (===== Título =====)
        wikiText = wikiText.replace(/=====\s(.*?)\s=====/g, '<h5>$1</h5>');

        // Encuentra y reemplaza los encabezados de nivel 3 (==== Título ====)
        wikiText = wikiText.replace(/====\s(.*?)\s====/g, '<h4>$1</h4>');

        // Encuentra y reemplaza los encabezados de nivel 2 (=== Título ===)
        wikiText = wikiText.replace(/===\s(.*?)\s===/g, '<h3>$1</h3>');


        // Encuentra y reemplaza los encabezados de nivel 1 (== Título ==)
        wikiText = wikiText.replace(/==\s(.*?)\s==/g, '<h2>$1</h2>');








        // Encuentra y reemplaza los enlaces ([[Texto|URL]])
        wikiText = wikiText.replace(/\[\[(.*?)\|(.*?)\]\]/g, '<a href="$2">$1</a>');

        // ... (otros reemplazos)

        return wikiText;
    }

    const wikiText = documento.wikitext

    const html = wikiTextToHtml(wikiText);

    // Ahora, puedes insertar el HTML resultante en un elemento en tu página web




    return (
        <div className="login-screen-view">
            <div className="document-complete-frame">
                <h1>{documento.title}</h1>
                <div id="contenido">

                </div>
            </div>
        </div>
    );
}