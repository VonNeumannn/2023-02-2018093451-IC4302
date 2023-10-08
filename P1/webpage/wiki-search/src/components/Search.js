import React, { useRef, useEffect } from "react";
import '../App.css';
import Facet from "./Facet";
import Document from "./Document";
import { createRoot } from 'react-dom';
import Looking from "./Looking";

export default function Search() {
    const containerRef = useRef(null);
    const containerRef2 = useRef(null);
    var somethingSearched = false

    const onClickHandler = () => {
        const miDiv = document.getElementById("miDiv");
        miDiv.innerHTML = "";

        let daysHTML = [];
        for (var element of documentos.documents) {
            daysHTML.push(
                <Document
                    title={element.title}
                    text={element.plaintext}
                />
            );
        }

        // Renderizar el componente solo si hay datos en el array
        if (daysHTML.length > 0) {
            const root = createRoot(containerRef2.current);
            root.render(<>{daysHTML}</>);
        }


        daysHTML = [];
        for (var element of facets.facets) {
            daysHTML.push(
                <Facet
                    name={element.category}
                    options={element.values}
                />
            );
        }


        // Renderizar el componente solo si hay datos en el array
        if (daysHTML.length > 0) {
            const root = createRoot(containerRef.current);
            root.render(<>{daysHTML}</>);
        }
    }

    const facets = {
        "facets": [
            {
                "category": "Color",
                "values": [
                    {
                        "name": "Rojo",
                        "count": 25,
                        "color_code": "#FF0000"
                    },
                    {
                        "name": "Azul",
                        "count": 18,
                        "color_code": "#0000FF"
                    },
                    {
                        "name": "Verde",
                        "count": 12,
                        "color_code": "#00FF00"
                    }
                ]
            },
            {
                "category": "Tamaño",
                "values": [
                    {
                        "name": "Pequeño",
                        "count": 30,
                        "description": "Menos de 10 cm"
                    },
                    {
                        "name": "Mediano",
                        "count": 20,
                        "description": "Entre 10 cm y 20 cm"
                    },
                    {
                        "name": "Grande",
                        "count": 15,
                        "description": "Más de 20 cm"
                    }
                ]
            },
            {
                "category": "Precio",
                "values": [
                    {
                        "name": "$10 - $20",
                        "count": 40,
                        "range": [10, 20]
                    },
                    {
                        "name": "$20 - $30",
                        "count": 22,
                        "range": [20, 30]
                    },
                    {
                        "name": "$30 - $50",
                        "count": 18,
                        "range": [30, 50]
                    }
                ]
            },
            {
                "category": "Color",
                "values": [
                    {
                        "name": "Rojo",
                        "count": 25,
                        "color_code": "#FF0000"
                    },
                    {
                        "name": "Azul",
                        "count": 18,
                        "color_code": "#0000FF"
                    },
                    {
                        "name": "Verde",
                        "count": 12,
                        "color_code": "#00FF00"
                    }
                ]
            },
            {
                "category": "Tamaño",
                "values": [
                    {
                        "name": "Pequeño",
                        "count": 30,
                        "description": "Menos de 10 cm"
                    },
                    {
                        "name": "Mediano",
                        "count": 20,
                        "description": "Entre 10 cm y 20 cm"
                    },
                    {
                        "name": "Grande",
                        "count": 15,
                        "description": "Más de 20 cm"
                    }
                ]
            },
            {
                "category": "Precio",
                "values": [
                    {
                        "name": "$10 - $20",
                        "count": 40,
                        "range": [10, 20]
                    },
                    {
                        "name": "$20 - $30",
                        "count": 22,
                        "range": [20, 30]
                    },
                    {
                        "name": "$30 - $50",
                        "count": 18,
                        "range": [30, 50]
                    }
                ]
            }
        ]
    }

    const documentos = {
        "documents": [
            {
                "title": "Einstein",
                "wikitext": "== Albert Einstein ==\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\n=== Early Life ===\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\n=== Theory of Relativity ===\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\n=== Later Life ===\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.\n",
                "plaintext": "Albert Einstein\n\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\nEarly Life\n\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\nTheory of Relativity\n\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\nLater Life\n\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism."
            },

            {
                "title": "Einstein",
                "wikitext": "== Albert Einstein ==\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\n=== Early Life ===\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\n=== Theory of Relativity ===\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\n=== Later Life ===\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.\n",
                "plaintext": "Albert Einstein\n\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\nEarly Life\n\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\nTheory of Relativity\n\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\nLater Life\n\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism."
            }


        ]
    }

    function callItems() {

    }
    function callItems2() {
        const daysHTML = [];

        daysHTML.push(
            <Looking />
        );


        // Renderizar el componente solo si hay datos en el array
        if (daysHTML.length > 0) {
            const root = createRoot(containerRef2.current);
            root.render(<>{daysHTML}</>);
        }
    }

    useEffect(() => {
        somethingSearched ? callItems() : callItems2()
    }, [somethingSearched]);
    return (
        <div className="login-screen-view">
            <div className="search-frame">
                <h1>Buscador WikiSearch</h1>

                <div className="search-space">
                    <input type="text" placeholder="Búsqueda" autoFocus required className="search-var" />
                    <button className="button-search" onClick={onClickHandler}>Buscar</button>
                </div>

                <div className="content-frame">
                    <div className="facets-frame" ref={containerRef}>

                    </div>

                    <div id="miDiv" className="document-frame" ref={containerRef2}>

                    </div>
                </div>
            </div>



        </div>
    );
}