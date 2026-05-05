import pytest
import pandas as pd
from unittest.mock import patch
from src.crypto_prices.data_transformation import transform_crypto_price_data


class TestTransformCryptoPriceData:
    """Tests for the transform_crypto_price_data function"""
    
    @patch('src.crypto_prices.data_transformation.current_time', '2026-05-05 10:00:00')
    def test_transform_crypto_price_data_success(self):
        """Test successful transformation of crypto price data"""
        # Arrange
        input_data = {
            'bitcoin': {'usd': 45000.50},
            'ethereum': {'usd': 2500.25},
        }
        
        # Act
        result = transform_crypto_price_data(input_data)
        
        # Assert
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert 'coin_id' in result.columns
        assert 'price_usd' in result.columns
        assert 'timestamp' in result.columns
        assert result.iloc[0]['price_usd'] == 45000.50
    
    def test_transform_crypto_price_data_none_input(self):
        """Test handling of None input"""
        # Act
        result = transform_crypto_price_data(None)
        
        # Assert
        assert result is None
    
    @patch('src.crypto_prices.data_transformation.current_time', '2026-05-05 10:00:00')
    def test_transform_crypto_price_data_single_record(self):
        """Test transformation with single record"""
        # Arrange
        input_data = {'bitcoin': {'usd': 45000}}
        
        # Act
        result = transform_crypto_price_data(input_data)
        
        # Assert
        assert len(result) == 1
        assert result.iloc[0]['coin_id'] == 'bitcoin'
        assert result.iloc[0]['price_usd'] == 45000
    
    @patch('src.crypto_prices.data_transformation.current_time', '2026-05-05 10:00:00')
    def test_transform_crypto_price_data_timestamp(self):
        """Test that timestamp is added correctly"""
        # Arrange
        input_data = {'bitcoin': {'usd': 45000}}
        
        # Act
        result = transform_crypto_price_data(input_data)
        
        # Assert
        assert result.iloc[0]['timestamp'] == '2026-05-05 10:00:00'
    
    def test_transform_crypto_price_data_empty_dict(self):
        """Test handling of empty dictionary"""
        # Act
        result = transform_crypto_price_data({})
        
        # Assert
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
    
    def test_transform_crypto_price_data_missing_usd_key(self):
        """Test handling of missing 'usd' key"""
        # Arrange
        input_data = {'bitcoin': {'eur': 40000}}
        
        # Act & Assert
        with pytest.raises(KeyError):
            transform_crypto_price_data(input_data)
