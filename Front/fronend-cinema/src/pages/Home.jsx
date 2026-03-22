import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiUrl } from '../config/api';

const Home = () => {
  const [filmes, setFilmes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const buscarFilmes = async () => {
      try {
        const response = await fetch(apiUrl('/api/filmes/'));
        const data = await response.json();
        
        // O Django REST geralmente pagina os resultados (colocando-os dentro de 'results')
        // Se não estiver paginado, a API retorna o array direto. O código abaixo lida com os dois casos.
        setFilmes(data.results ? data.results : data);
      } catch (error) {
        console.error("Erro ao buscar filmes:", error);
      } finally {
        setLoading(false);
      }
    };

    buscarFilmes();
  }, []);

  if (loading) return <p style={{ padding: '20px' }}>Carregando filmes...</p>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Filmes em Cartaz</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        {filmes.map((filme) => (
          <div key={filme.id} style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px' }}>
            <h3>{filme.titulo}</h3>
            <p><strong>Duração:</strong> {filme.duracao} minutos</p>
            {filme.em_cartaz ? (
              <Link 
                to={`/filme/${filme.id}/sessoes`} 
                style={{ background: '#007bff', color: 'white', padding: '8px 12px', textDecoration: 'none', borderRadius: '4px', display: 'inline-block' }}
              >
                Ver Horários e Sessões
              </Link>
            ) : (
              <span style={{ color: 'red' }}>Fora de cartaz</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;