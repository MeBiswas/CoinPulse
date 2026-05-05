import pytest
import pandas as pd
from src.crypto_coins.transformer import transform_coin_data


class TestTransformCoinData:
    """Tests for the transform_coin_data function"""
    
    def test_transform_coin_data_success(self):
        """Test successful transformation of coin data"""
        # Arrange
        input_data = [
            {'id': '1', 'symbol': 'BTC', 'name': 'Bitcoin'},
            {'id': '2', 'symbol': 'ETH', 'name': 'Ethereum'},
        ]
        
        # Act
        result = transform_coin_data(input_data)
        
        # Assert
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['coin_id', 'symbol', 'name']
        assert len(result) == 2
        assert result.iloc[0]['coin_id'] == '1'
        assert result.iloc[0]['symbol'] == 'BTC'
    
    def test_transform_coin_data_none_input(self):
        """Test handling of None input"""
        # Act
        result = transform_coin_data(None)
        
        # Assert
        assert result is None
    
    def test_transform_coin_data_empty_list(self):
        """Test handling of empty list"""
        # Act
        result = transform_coin_data([])
        # Assert
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
    
    def test_transform_coin_data_single_record(self):
        """Test transformation with single record"""
        # Arrange
        input_data = [{'id': '1', 'symbol': 'BTC', 'name': 'Bitcoin'}]
        
        # Act
        result = transform_coin_data(input_data)
        
        # Assert
        assert len(result) == 1
        assert result.iloc[0]['coin_id'] == '1'
    
    def test_transform_coin_data_column_rename(self):
        """Test that 'id' column is renamed to 'coin_id'"""
        # Arrange
        input_data = [{'id': '123', 'symbol': 'XYZ', 'name': 'Test Coin'}]
        
        # Act
        result = transform_coin_data(input_data)
        
        # Assert
        assert 'coin_id' in result.columns
        assert 'id' not in result.columns
        assert result.iloc[0]['coin_id'] == '123'
    
    def test_transform_coin_data_missing_columns(self):
        """Test handling of missing required columns"""
        # Arrange - missing 'name' column
        input_data = [{'id': '1', 'symbol': 'BTC'}]
        
        # Act & Assert - should raise an exception
        with pytest.raises(KeyError):
            transform_coin_data(input_data)
