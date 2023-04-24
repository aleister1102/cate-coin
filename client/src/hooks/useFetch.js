import { useState, useEffect } from 'react'

export default function useFetch(url){
    const [data, setData] = useState([])

    useEffect(() => {
        fetch(url)
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                setTimeout(() => {
                    setData(data)
                }, 0)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [url])

    return data
}

