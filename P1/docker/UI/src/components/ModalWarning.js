import Warning from '../assets/warning.png'; 
import React from 'react';
export default function ModalWarning(props) {
    return(
        <div className="modal-warning" id="modal-warning">
                <dialog open id="modalWarning">
                    <div className="border-modal-warning">
                    </div>
                    <div className="logo-modal">
                        <img src={Warning} alt="warning" />
                    </div>
                    <p>{props.text}</p>
                </dialog>
            </div>
    );
}