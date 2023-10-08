import React, { useRef, useEffect } from "react";
import '../App.css';

import { createRoot } from 'react-dom';

export default function Document(props) {

    function resaltarFrase(texto, frase) {
        // Utilizamos una expresión regular con el modificador 'g' para buscar todas las ocurrencias de la frase
        const expresionRegular = new RegExp(frase, 'g');

        // Reemplazamos todas las ocurrencias de la frase con la frase rodeada por las etiquetas <mark>
        const textoResaltado = texto.replace(expresionRegular, "<mark>" + frase + "</mark>");

        return textoResaltado;
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

    const title = props.title;

    const containerRef = useRef(null);
    useEffect(() => {

        let text = encontrarContexto(props.text,title);
        text = resaltarFrase(text, title)
        const textoResaltado = text
        const daysHTML = [];
        daysHTML.push(
            <div key={title}>
                <h2 className="title-document"><a href={"/result/" + title} target="_parent">{title}</a></h2>
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