import Error from '../assets/error.png';
import React from 'react';
export default function ModalError() {
    return(
        <div className="modal-container" id="modal-container">
                <dialog open id="modal">
                    <div className="border-modal">
                    </div>
                    <div className="logo-modal">
                        <img src={Error} alt="error-image" />
                    </div>

                    <p>Hubo un error al intentar conectar con la base de datos, favor intentar de nuevo.</p>
                </dialog>
            </div>
    );
}