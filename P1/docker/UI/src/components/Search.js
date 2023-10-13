import React, { useRef, useEffect, useState} from "react";
import "../App.css";
import Facet from "./Facet";
import Document from "./Document";
import { createRoot } from "react-dom";
import { useNavigate } from "react-router-dom";
import Looking from "./Looking";
import axios from "axios";
import ModalInfo from "./ModalInfo";
import ModalWarning from "./ModalWarning";

export default function Search() {
  const containerRef = useRef(null);
  const containerRef2 = useRef(null);
  var somethingSearched = false;
  var tipoDB;
  const [array, setArray] = useState([]);
  const [arrayFacets, setArrayFacets] = useState([]);
  const navigate = useNavigate();
  document.title = "Buscar"

  
  const OnClickHandler = () => {
    const search = document.getElementById("searching").value;
    const modalInfo = document.getElementById("modal-info")
    const modalWarning = document.getElementById("modal-warning")
    if(modalWarning.classList.value.includes("mostrando")){
      modalWarning.classList.remove('mostrando')
      modalWarning.classList.add('ocultando')
    }
    modalInfo.classList.remove('ocultando')
    modalInfo.classList.add('mostrando')
    if (search.trim() === "") {
      alert("Debe agregar algun parámetro de búsqueda");
    } else {
      const miDiv = document.getElementById("miDiv");
      const miDiv2 = document.getElementById("facets-frame");
      miDiv.innerHTML = "";
      miDiv2.innerHTML = "";
      var mensajeError = document.getElementById("mensaje-error");

      const radios = document.getElementsByName("opcion");
      // Iterar a través de los elementos de radio para encontrar el seleccionado
      
      for (const radio of radios) {
        if (radio.checked) {
          tipoDB = radio.value;
          break; // Salir del bucle cuando se encuentre el seleccionado
        }
      }
      console.log("Valor seleccionado:", tipoDB);

      const apiUrl =
        "http://172.17.0.2:5000/search?stringBusqueda=" +
        search +
        "&tipoRecurso=" +
        tipoDB;

      //Realizar la solicitud POST
      axios
        .get(apiUrl)
        .then((response) => {
          if (response.status) {
            console.log(response.data[1][0].facet)
            setArray(response.data[0]);
            setArrayFacets(response.data[1][0].facet)
            modalInfo.classList.remove('mostrando')
            modalInfo.classList.add('ocultando')

            
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

          modalInfo.classList.remove('mostrando')
          modalInfo.classList.add('ocultando')
          modalWarning.classList.remove('ocultando')
          modalWarning.classList.add('mostrando')

         

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
  
//////////////DOCUMENTS
  useEffect(() => {
    if (array.length > 0) {
      const search = document.getElementById("searching").value;
      let daysHTML = [];

      for (let i = 0; i < array.length; i++) {
        try {
          let a = array[i]
          const radios = document.getElementsByName("opcion");
      // Iterar a través de los elementos de radio para encontrar el seleccionado
      
      for (const radio of radios) {
        if (radio.checked) {
          tipoDB = radio.value;
          break; // Salir del bucle cuando se encuentre el seleccionado
        }
      }
          console.log("------------------------",tipoDB)
          daysHTML.push(
            <Document
              title={array[i].Title.toString()}
              text={array[i].highlights[0].texts}
              searched = {search}
              database = {tipoDB}
              navigate={navigate}
              
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


 /////////////////FACETS
 useEffect(() => {
  console.log("Quiero ser el rey");
  console.log(arrayFacets)
  if (Object.keys(arrayFacets).length > 0) {
    const search = document.getElementById("searching").value;
    let daysHTML = [];
    let tipoDB = ""; // Declarar tipoDB antes de usarlo

    const radios = document.getElementsByName("opcion");

    // Iterar a través de los elementos de radio para encontrar el seleccionado
    for (const radio of radios) {
      if (radio.checked) {
        tipoDB = radio.value;
        break; // Salir del bucle cuando se encuentre el seleccionado
      }
    }

    // Iterar sobre las propiedades del objeto arrayFacets
    for (const clave in arrayFacets) {
      if (arrayFacets.hasOwnProperty(clave)) {
        console.log("Nombre de la clave:", clave);
        console.log("Valores:");
        const valoresInternos = arrayFacets[clave].buckets;
        console.log(valoresInternos)
        daysHTML.push(
          <Facet
            name={clave}
            options={valoresInternos}
            searched={search}
            database={tipoDB}
          />
        );
      }
    }

    // Renderizar el componente solo si hay datos en el array
    if (daysHTML.length > 0) {
      const root = createRoot(containerRef.current);
      root.render(<>{daysHTML}</>);
    }
  }

  console.log("HOLIIIIIIIIIII FACETS");
}, [arrayFacets]);



  

  useEffect(() => {
    const inputElement = document.getElementById('searching');

    // Agrega un event listener al elemento input
    inputElement.addEventListener('keydown', function(event) {
    // Verifica si la tecla presionada es "Enter" (código de tecla 13)
    if (event.keyCode === 13) {
        // Realiza la acción que deseas cuando se presiona "Enter"
        OnClickHandler()
        // Puedes reemplazar el alert con la acción que desees realizar.
    }
});
    
}, [somethingSearched]);


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
        <ModalInfo text={"Buscando su archivo, espere un momento"}/>
        <ModalWarning text={"No se encontro su archivo, intente buscando con otras palabras"}/>

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
          
          <div className="facets-frame" id="facets-frame" ref={containerRef}></div>
          

          <div id="miDiv" className="document-frame" ref={containerRef2}>
            
          </div>
        </div>
      </div>
    </div>
  );
}
