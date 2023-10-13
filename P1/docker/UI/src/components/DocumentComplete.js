import React, { useEffect, useState } from "react";
import axios from 'axios'

export default function DocumentComplete() {
        const [myJson, setJson] = useState({});
        const [isLoading, setLoading] = useState(true);
      
        // Obtiene la URL actual del navegador
        const urlActual = window.location.href;
      
        // Divide la URL en partes usando '/' como separador y toma la última parte
        const partesDeLaURL = urlActual.split('/');
        const ultimaParteDeLaURL = partesDeLaURL.pop();
        const titulo = ultimaParteDeLaURL.split('&')[0];
        const base = ultimaParteDeLaURL.split('&')[1];
        const tituloCambiado=titulo.replace(/-/g, " ")
        document.title = tituloCambiado
      
        useEffect(() => {
          const apiUrl =
            "http://127.0.0.1:5000/document?titulo=" +
            tituloCambiado +
            "&tipoRecurso=" +
            base;
      
          // Realizar la solicitud POST dentro del useEffect
          axios
            .get(apiUrl)
            .then((response) => {
              if (response.status) {
                setJson(response.data);
                console.log(response);
              } else {
                alert("Error en la solicitud");
              }
            })
            .catch((error) => {
              // Manejar errores de la solicitud
              console.error("Error en la solicitud:", error);
            })
            .finally(() => {
              // Indicar que la carga ha finalizado
              setLoading(false);
            });
        }, [titulo, base]); // Dependencias que desencadenarán la llamada al API
      
        useEffect(() => {
          try {
            if (!isLoading && myJson.wikiText) {
              const html = wikiToHtml(myJson.wikiText);
              document.getElementById("contenido").innerHTML = resaltarFrase(html, titulo);
            }
          } catch (error) {
            console.error(error);
          }
        }, [isLoading, myJson, titulo]);

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

  function convertFromWikiTextToHtml(wikiText) {
    
  }

    function wikiToHtml(wikiText) {
        let htmlText = wikiText;
    
        // Convertir negrita
        htmlText = htmlText.replace(/'''(.*?)'''/g, '<b>$1</b>');
    
        // Convertir cursiva
        htmlText = htmlText.replace(/''(.*?)''/g, '<i>$1</i>');
    
        // Convertir encabezados
        for(let i=6; i>0; i--) {
            let equals = '='.repeat(i);
            let h = 'h' + i;
            let re = new RegExp('^' + equals + '(.*?)' + equals + '$', 'gm');
            htmlText = htmlText.replace(re, '<'+h+'>$1</'+h+'>');
        }
    
        // Convertir enlaces internos
        htmlText = htmlText.replace(/\[\[(.*?)\]\]/g, function(match, p1) {
            let parts = p1.split('|');
            if(parts.length == 2) {
                return '<a href="' + parts[0] + '">' + parts[1] + '</a>';
            } else {
                return '<a href="' + parts[0] + '">' + parts[0] + '</a>';
            }
        });
    
        // Convertir enlaces externos
        htmlText = htmlText.replace(/\[(http.*?) (.*?)\]/g, '<a href="$1">$2</a>');
    
        // Convertir listas sin orden
        htmlText = htmlText.replace(/^(\*.*\n)+/gm, function(match) {
            return '<ul>\n' + match.replace(/^\*(.*)\n/gm, '<li>$1</li>\n') + '</ul>\n';
        });
    
        // Convertir listas ordenadas
        htmlText = htmlText.replace(/^(\#.*\n)+/gm, function(match) {
            return '<ol>\n' + match.replace(/^\#(.*)\n/gm, '<li>$1</li>\n') + '</ol>\n';
        });
    
        // Convertir citas
        htmlText = htmlText.replace(/^:(.*?)(?=\n\n|$)/gm, '<blockquote>$1</blockquote>');
    
        // Convertir lÃ­neas horizontales
        htmlText = htmlText.replace(/^----$/gm, '<hr>');

        htmlText = htmlText.replace(/<pre>([\s\S]*?)<\/pre>/g, function(match, p1) {
            return '<pre>' + p1.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
        });

        htmlText = htmlText.replace(/[[File:(.*?)]]/g, '<img src="$1">');
    

        return htmlText;
    }


    

    // Ahora, puedes insertar el HTML resultante en un elemento en tu página web




    return (
        <div className="login-screen-view">
            <div className="document-complete-frame">
            
                <a id="linkMain" target="_blank" href={myJson.wikiLink}>{titulo.replace(/-/g, " ")}</a>
                <div id="contenido">

                </div>
            </div>
        </div>
    );
}