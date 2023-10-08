import React, { useRef, useEffect, useState} from "react";
import "../App.css";
import Facet from "./Facet";
import Document from "./Document";
import { createRoot } from "react-dom";
import Looking from "./Looking";
import axios from "axios";

export default function Search() {
  const containerRef = useRef(null);
  const containerRef2 = useRef(null);
  var somethingSearched = false;
  var tipoDB;
  const [array, setArray] = useState([]);
  const OnClickHandler = () => {
    
    const search = document.getElementById("searching").value;
    if (search.trim() === "") {
      alert("Debe agregar algun parámetro de búsqueda");
    } else {
      const miDiv = document.getElementById("miDiv");
      miDiv.innerHTML = "";

      const radios = document.getElementsByName("opcion");
      var mensajeError = document.getElementById("mensaje-error");
      // Iterar a través de los elementos de radio para encontrar el seleccionado
      
      for (const radio of radios) {
        if (radio.checked) {
          tipoDB = radio.value;
          break; // Salir del bucle cuando se encuentre el seleccionado
        }
      }
      console.log("Valor seleccionado:", tipoDB);

      const apiUrl =
        "http://127.0.0.1:5000/search?stringBusqueda=" +
        search +
        "&tipoRecurso=" +
        tipoDB;

      //Realizar la solicitud POST
      axios
        .get(apiUrl)
        .then((response) => {
          if (response.status) {
            setArray(response.data[0]);
            mensajeError.textContent = ""
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
          
         
          mensajeError.textContent = "No se encontraron resultados";
        });
    }
  };

  function dividirCadenaEn4Partes(cadena) {
    if (cadena.length < 20) {
      // La cadena es demasiado corta para dividirla en 4 partes
      return [cadena];
    }
  
    const longitud = Math.ceil(cadena.length / 20); // Calcular la longitud de cada parte
    const partes = [];
  
    for (let i = 0; i < 20; i++) {
      const inicio = i * longitud;
      const fin = (i + 1) * longitud;
      partes.push(cadena.substring(inicio, fin));
    }
  
    return partes;
  }
  

  useEffect(() => {
    if (array.length > 0) {
      const search = document.getElementById("searching").value;
      let daysHTML = [];

      for (let i = 0; i < array.length; i++) {
        try {
          let a = array[i]
          daysHTML.push(
            <Document
              title={array[i].Title.toString()}
              text={array[i].highlights[0].texts}
              searched = {search}
              database = {tipoDB}
            />
          );
        } catch (error) {
          console.log(array[i])
          console.error(error)
        }
        
      }
  
      // Renderizar el componente solo si hay datos en el array
      if (daysHTML.length > 0) {
        const root = createRoot(containerRef2.current);
        root.render(<>{daysHTML}</>);
      }
    }
  }, [array]);

  const facets = {
    facets: [
      {
        category: "Color",
        values: [
          {
            name: "Rojo",
            count: 25,
            color_code: "#FF0000",
          },
          {
            name: "Azul",
            count: 18,
            color_code: "#0000FF",
          },
          {
            name: "Verde",
            count: 12,
            color_code: "#00FF00",
          },
        ],
      },
      {
        category: "Tamaño",
        values: [
          {
            name: "Pequeño",
            count: 30,
            description: "Menos de 10 cm",
          },
          {
            name: "Mediano",
            count: 20,
            description: "Entre 10 cm y 20 cm",
          },
          {
            name: "Grande",
            count: 15,
            description: "Más de 20 cm",
          },
        ],
      },
      {
        category: "Precio",
        values: [
          {
            name: "$10 - $20",
            count: 40,
            range: [10, 20],
          },
          {
            name: "$20 - $30",
            count: 22,
            range: [20, 30],
          },
          {
            name: "$30 - $50",
            count: 18,
            range: [30, 50],
          },
        ],
      },
      {
        category: "Color",
        values: [
          {
            name: "Rojo",
            count: 25,
            color_code: "#FF0000",
          },
          {
            name: "Azul",
            count: 18,
            color_code: "#0000FF",
          },
          {
            name: "Verde",
            count: 12,
            color_code: "#00FF00",
          },
        ],
      },
      {
        category: "Tamaño",
        values: [
          {
            name: "Pequeño",
            count: 30,
            description: "Menos de 10 cm",
          },
          {
            name: "Mediano",
            count: 20,
            description: "Entre 10 cm y 20 cm",
          },
          {
            name: "Grande",
            count: 15,
            description: "Más de 20 cm",
          },
        ],
      },
      {
        category: "Precio",
        values: [
          {
            name: "$10 - $20",
            count: 40,
            range: [10, 20],
          },
          {
            name: "$20 - $30",
            count: 22,
            range: [20, 30],
          },
          {
            name: "$30 - $50",
            count: 18,
            range: [30, 50],
          },
        ],
      },
    ],
  };

  //const documentos = {
  //  documents: [
  //    {
  //      title: "Einstein",
  //      wikitext:
  //        "== Albert Einstein ==\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\n=== Early Life ===\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\n=== Theory of Relativity ===\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\n=== Later Life ===\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.\n",
  //      plaintext:
  //        "Albert Einstein\n\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\nEarly Life\n\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\nTheory of Relativity\n\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\nLater Life\n\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.",
  //    },
  //
  //    {
  //      title: "Einstein",
  //      wikitext:
  //        "== Albert Einstein ==\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\n=== Early Life ===\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\n=== Theory of Relativity ===\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\n=== Later Life ===\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.\n",
  //      plaintext:
  //        "Albert Einstein\n\nAlbert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. His work is also known for its influence on the philosophy of science.\n\nEarly Life\n\nEinstein was born in Ulm, Germany, in 1879. He showed an early aptitude for mathematics and physics and later studied at the Swiss Federal Polytechnic.\n\nTheory of Relativity\n\nEinstein's theory of relativity revolutionized our understanding of space, time, and gravity. His famous equation, E=mc^2, is well-known around the world.\n\nLater Life\n\nEinstein emigrated to the United States in the 1930s to escape the rise of the Nazis in Germany. He became a professor at Princeton University and continued his work in physics and activism.",
  //    },
  //  ],
  //};

  function callItems() {}
  function callItems2() {
    const daysHTML = [];

    daysHTML.push(<Looking />);

    // Renderizar el componente solo si hay datos en el array
    if (daysHTML.length > 0) {
      const root = createRoot(containerRef2.current);
      root.render(<>{daysHTML}</>);
    }
  }

  useEffect(() => {
    somethingSearched ? callItems() : callItems2();
  }, [somethingSearched]);
  return (
    <div className="login-screen-view">
      <div className="search-frame">
        <h1>Buscador WikiSearch</h1>

        <div className="search-space">
          <input
            id="searching"
            placeholder="Búsqueda"
            autoFocus
            required
            className="search-var"
          />
          <button className="button-search" onClick={OnClickHandler}>
            Buscar
          </button>
        </div>
        <div className="round-buttons">
          <label>
            <input type="radio" name="opcion" value={2} checked /> Mongo Atlas
          </label>

          <label>
            <input type="radio" name="opcion" value={1} /> Autonomous SQL
          </label>
        </div>
        <p id="mensaje-error" className="mensaje-error2"></p>
        <div className="content-frame">
          
          <div className="facets-frame" ref={containerRef}></div>
          

          <div id="miDiv" className="document-frame" ref={containerRef2}>
            
          </div>
        </div>
      </div>
    </div>
  );
}
