import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const ListaSessoes = () => {
  // Pega o ID do filme que está na URL
  const { filmeId } = useParams();
  const [sessoes, setSessoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const buscarSessoes = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/filmes/${filmeId}/sessoes/`);
        const data = await response.json();
        setSessoes(data);
      } catch (error) {
        console.error("Erro ao buscar sessões:", error);
      } finally {
        setLoading(false);
      }
    };

    buscarSessoes();
  }, [filmeId]);

  if (loading) return <p style={{ padding: '20px' }}>Carregando horários...</p>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Sessões Disponíveis</h2>
      <Link to="/" style={{ color: '#007bff', textDecoration: 'none', marginBottom: '20px', display: 'inline-block' }}>
        &larr; Voltar para filmes
      </Link>

      {sessoes.length === 0 ? (
        <p>Nenhuma sessão disponível para este filme no momento.</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '15px' }}>
          {sessoes.map((sessao) => {
            // Formata a data e hora para ficar amigável
            const dataHora = new Date(sessao.horario_inicio).toLocaleString('pt-BR');

            return (
              <div key={sessao.id} style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px', background: '#f9f9f9' }}>
                <h4 style={{ margin: '0 0 10px 0' }}>{sessao.sala_nome}</h4>
                <p style={{ margin: '5px 0' }}><strong>Início:</strong> {dataHora}</p>
                <p style={{ margin: '5px 0', color: 'green' }}>
                  <strong>Assentos Livres:</strong> {sessao.assentos_disponiveis}
                </p>
                <Link 
                  to={`/sessao/${sessao.id}/comprar`}
                  style={{ background: '#28a745', color: 'white', padding: '8px 12px', textDecoration: 'none', borderRadius: '4px', display: 'block', textAlign: 'center', marginTop: '10px' }}
                >
                  Escolher Assento
                </Link>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ListaSessoes;