import React, { useRef, useEffect } from "react";
import '../App.css';

import { createRoot } from 'react-dom';

export default function Facet(props) {
    const containerRef = useRef(null);
    useEffect(() => {
        const name = props.name;
        const arrayOptions = props.options;

        const daysHTML = [];
        daysHTML.push(<span className="tittle-facet">{name}</span>)
        for (var element of arrayOptions) {
            daysHTML.push(
                <div key={element.name}>
                    <input type="checkbox" id={element.name} value={element.value} className="inputs-facets"/>
                    <label htmlFor={element.name}>{element.name}</label>
                    
                </div>
            );
        }

        // Renderizar el componente solo si hay datos en el array
        if (daysHTML.length > 0) {
            const root = createRoot(containerRef.current);
            root.render(<>{daysHTML}</>);
        }
    }, [props]);

    return(
        <div className="facet-square" >
           <div className="facets-options" ref={containerRef}>

           </div>

        </div>
    );
}