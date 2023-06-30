import {useState, useEffect} from 'react';
import axios from "axios";


const ArtistsDetail = (props) => {

    const [artist, setArtist] = useState(null);
    useEffect(() => {

        axios.get(`http://127.0.0.1:8000/api/v1/audio/artists/${props.artistId}/`)
        .then(response => setArtist(response.data))
        .catch(error => console.log(error));
    }, [props.artistId])

    if (!artist) {
        return <div>Loading..</div>;
    }

    return (
        <div className="artist">
            <h1>{artist.name}</h1>
            <p>{artist.bio}</p>
        </div>
    )
}

export default ArtistsDetail;