import React, { useEffect } from "react";


export default function DocumentComplete() {
    function resaltarFrase(texto, frase) {
        // Utilizamos una expresión regular con el modificador 'g' para buscar todas las ocurrencias de la frase
        const expresionRegular = new RegExp(frase, 'g');

        // Reemplazamos todas las ocurrencias de la frase con la frase rodeada por las etiquetas <mark>
        const textoResaltado = texto.replace(expresionRegular, "<mark>" + frase + "</mark>");

        return textoResaltado;
    }
    const documento = {
        "title": "Einstein",
        "wikitext": "== Albert Einstein ==\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\n=== Early Life ===\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\n=== Theory of Relativity ===\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\n=== Later Life ===\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.\n",
        "plaintext": "Albert Einstein\n\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\nEarly Life\n\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\nTheory of Relativity\n\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\nLater Life\n\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism."
    }

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

    useEffect(() => {
        document.getElementById("contenido").innerHTML = resaltarFrase(html,documento.title);
    }, [html]);


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