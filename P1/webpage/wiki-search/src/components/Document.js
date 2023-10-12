import React, { useRef, useEffect } from "react";
import '../App.css';

import { createRoot } from 'react-dom';
import { useNavigate } from 'react-router-dom';

export default function Document(props) {
    //console.log(props.title+" + "+props.text)
    const navigate=props.navigate
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

    function textMerge(array) {
        let text = "";
        for (let i = 0; i < array.length; i++) {
            text += array[i].value + " ";
        }
        return text
    }

    

    function buscarYCapturarContexto(arr, fraseABuscar) {
        let contador = 0; // Inicializamos un contador para llevar el seguimiento de cuántas veces se ha encontrado la frase.
        const contexto = []; // Array para almacenar los contextos.
      
        for (let i = 0; i < arr.length; i++) {
          const cadena = arr[i];
      
          if (cadena.includes(fraseABuscar)) {
            contador++;
      
            const palabras = cadena.split(" "); // Dividimos la cadena en palabras.
            const indiceFrase = palabras.indexOf(fraseABuscar); // Encontramos el índice de la frase en la lista de palabras.
      
            // Capturamos el contexto de 10 palabras antes y después de la frase.
            const inicio = Math.max(0, indiceFrase - 10);
            const fin = Math.min(palabras.length, indiceFrase + 11);
            const contextoFrase = palabras.slice(inicio, fin).join(" ");
            contexto.push(contextoFrase);
      
            if (contador === 2) {
              break;
            }
          }
        }
      
        return contexto;
      }

    function encontrarContexto(texto, frase) {
        // Divide el texto en palabras
        const palabras = texto.split(' ');

        // Encuentra la segunda aparición de la frase
        let segundaAparicion = -1;
        let contador = 0;
        for (let i = 0; i < palabras.length; i++) {
            if (palabras[i].includes(frase)) {
                contador++;
                if (contador === 2) {
                    segundaAparicion = i;
                    break;
                }
            }
        }

        if (segundaAparicion === -1) {
            // No se encontró la segunda aparición de la frase
            return null;
        }

        // Toma 10 palabras antes y después de la segunda aparición
        const inicio = Math.max(0, segundaAparicion - 10);
        const fin = Math.min(palabras.length, segundaAparicion + 11);

        // Genera el contexto
        const contexto = palabras.slice(inicio, fin).join(' ');

        return contexto;
    }

    function cambiarURL(nuevaURL) {
        //const nuevaURL = '/nueva-ruta'; // La nueva URL que deseas utilizar
        //history.pushState(null, null, nuevaURL);
        navigate(nuevaURL)
      }

    const title = props.title;

    const containerRef = useRef(null);
    useEffect(() => {

        let texto = textMerge(props.text) //buscarYCapturarContexto(props.text, props.searched)//encontrarContexto(props.text,props.searched);
        texto = resaltarFrase(texto, props.searched)
        const textoResaltado = texto
        
        const daysHTML = [];
        daysHTML.push(
            <div key={title}>
                <h2 className="document-title"><span onClick={()=>cambiarURL("/result/" + title.replace(/ /g, "-")+"&"+props.database)}>{title}</span></h2>
                <div dangerouslySetInnerHTML={{ __html: textoResaltado }} />
            </div>

        );


        // Renderizar el componente solo si hay datos en el array
        if (daysHTML.length > 0) {
            const root = createRoot(containerRef.current);
            root.render(<>{daysHTML}</>);
        }
    }, [props]);

    return (
        <div className="document-square" ref={containerRef}>

        </div>
    );
}