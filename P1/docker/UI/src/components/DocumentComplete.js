import React, { useEffect, useState } from "react";
import ModalInfo from "./ModalInfo";
import Like from '../assets/like.png';
import Dislike from '../assets/dislike.png';

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
          const modalInfo = document.getElementById("modal-info")
          modalInfo.classList.add('mostrando')
          const apiUrl =
            "http://172.17.0.2:5000/document?title=" +
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
              const html = myJson.wikiText;
              document.getElementById("contenido").innerHTML = resaltarFrase(html, titulo);
              const modalInfo = document.getElementById("modal-info")
              modalInfo.classList.remove('mostrando')
              modalInfo.classList.add('ocultando')
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

  


    function OnClickRatings(rating){
      const counter = document.getElementById("counter")
      counter.innerHTML = parseInt(counter.innerHTML) + rating
    }


    

    // Ahora, puedes insertar el HTML resultante en un elemento en tu página web




    return (
        <div className="login-screen-view">
            <div className="document-complete-frame">
                <ModalInfo text={"Se está buscando su documento. Espere un momento por favor."} />
                <a id="linkMain" target="_blank" href={myJson.wikiLink}>{titulo.replace(/-/g, " ")}</a>
                <div className="content-frame">
                  <div className="rating-frame">
                    <div className="rating">
                      <h3 className="title-rating">Rating</h3>
                      <p className="rating-amount" id="counter">{myJson.rating}</p>
                      <div className="rating-buttons">
                        <img src={Like} alt="like buttom" onClick={()=>OnClickRatings(1)}/>
                        <img src={Dislike} alt="dislike buttom" onClick={()=>OnClickRatings(-1)}/>
                      </div>
                    </div>
                  </div>
                  
                  <div id="contenido">

                  </div>

                </div>
                

            </div>
        </div>
    );
}