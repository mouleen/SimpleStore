import React, { useState, useEffect } from 'react';
import { useGlobalHelpers } from "../hooks/useGlobalHelpers";

const StoreIndex = () => {
    // Datos básicos (Mock)
    const { mockCafeterias } = useGlobalHelpers();
    const [cafeterias, setCafeterias] = useState(mockCafeterias);

  // conectar con otros componentes
  const handleCafeteriaClick = (cafeteria) => {
    console.log('Cafetería seleccionada:', cafeteria);
    // LLamar otros comp
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#F6E0C4', minHeight: '100vh' }}>
      {/* Título */}
      <h1 style={{ textAlign: 'center', color: '#78350f', marginBottom: '30px' }}>
        Descubre Cafeterías Increíbles
      </h1>
      <p style={{ textAlign: 'center', color: '#78350f', marginBottom: '30px' }}>Encuentra el lugar perfecto para tu próximo café</p>

      {/* Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '20px',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        {cafeterias.map((cafeteria) => (
          <div
            key={cafeteria.id}
            onClick={() => handleCafeteriaClick(cafeteria)}
            style={{
              backgroundColor: 'white',
              borderRadius: '10px',
              overflow: 'hidden',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              cursor: 'pointer',
              transition: 'transform 0.2s'
            }}
            onMouseEnter={(e) => e.target.style.transform = 'translateY(-5px)'}
            onMouseLeave={(e) => e.target.style.transform = 'translateY(0)'}
          >
            {/* Imagen */}
            <img
              src={cafeteria.image}
              alt={cafeteria.name}
              style={{ width: '100%', height: '200px', objectFit: 'cover' }}
            />

            {/* Información básica */}
            <div style={{ padding: '15px' }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#78350f' }}>
                {cafeteria.name}
              </h3>
              <p style={{ margin: '0 0 10px 0', color: '#6b7280', fontSize: '14px' }}>
                📍 {cafeteria.location}
              </p>
              <p style={{ margin: '0', color: '#f97316', fontWeight: 'bold' }}>
                ⭐ {cafeteria.rating}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StoreIndex;