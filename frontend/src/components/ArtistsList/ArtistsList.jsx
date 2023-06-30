import {useState, useEffect} from "react";

import axios from "axios";
import { Link } from 'react-router-dom';

import ArtistsDetail from "../ArtistsDetail/ArtistsDetail";


const ArtistsList = () => {

    const [artists, setArtists] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/v1/audio/artists/")
        .then(response => {
            setArtists(response.data);
        })
    }, []);


    return (
        <div className="artists__block">
            {artists.map((artist) => (
                <div className="artist" key={artist.id}>
                    <img src={ artist.image } alt={artist.name}/>
                    <p>{ artist.name }</p>
                    <p>{artist.bio}</p>
                    <Link to={`/artists/${artist.id}`}>
                        <p>Посмотреть</p>
                    </Link>
                    <input type="text" o>
                </div>
            ))}
            
        </div>
    )
}

export default ArtistsList;