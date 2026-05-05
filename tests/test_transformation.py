import json
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, mock_open
from src.transformation import load_latest_file, save_processed


class TestLoadLatestFile:
    """Tests for the load_latest_file function"""
    
    @patch('src.transformation.glob')
    @patch('builtins.open', new_callable=mock_open, read_data='{"test": "data"}')
    def test_load_latest_file_success(self, mock_file, mock_glob):
        """Test successful loading of latest file"""
        # Arrange
        mock_glob.return_value = ['data/raw/coin_data/file1.json', 'data/raw/coin_data/file2.json']
        
        # Act
        result = load_latest_file('coin_data')
        
        # Assert
        assert result is not None
        assert result == {'test': 'data'}
        mock_file.assert_called_once()
    
    def test_load_latest_file_no_dataset_name(self):
        """Test handling of missing dataset name"""
        # Act
        result = load_latest_file(None)
        
        # Assert
        assert result is None
    
    def test_load_latest_file_empty_dataset_name(self):
        """Test handling of empty dataset name"""
        # Act
        result = load_latest_file('')
        
        # Assert
        assert result is None
    
    @patch('src.transformation.glob')
    def test_load_latest_file_not_found(self, mock_glob):
        """Test handling when no files are found"""
        # Arrange
        mock_glob.return_value = []
        
        # Act & Assert
        with pytest.raises((ValueError, Exception)):
            load_latest_file('coin_data')


class TestSaveProcessed:
    """Tests for the save_processed function"""
    
    @patch('src.transformation.PATHS')
    def test_save_processed_success(self, mock_paths):
        """Test successful saving of processed data"""
        # Arrange
        mock_output_dir = Path('/tmp/test_output')
        mock_paths.__getitem__.return_value = mock_output_dir
        
        df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        with patch.object(Path, 'mkdir'):
            with patch.object(pd.DataFrame, 'to_csv'):
                # Act
                result = save_processed(df, 'test_dataset')
        
        # Assert
        assert result is True
    
    def test_save_processed_none_dataframe(self):
        """Test handling of None dataframe"""
        # Act
        result = save_processed(None, 'test_dataset')
        
        # Assert
        assert result is None
    
    def test_save_processed_no_dataset_name(self):
        """Test handling of missing dataset name"""
        # Arrange
        df = pd.DataFrame({'col1': [1, 2]})
        
        # Act
        result = save_processed(df, None)
        
        # Assert
        assert result is None
    
    def test_save_processed_empty_dataset_name(self):
        """Test handling of empty dataset name"""
        # Arrange
        df = pd.DataFrame({'col1': [1, 2]})
        
        # Act
        result = save_processed(df, '')
        
        # Assert
        assert result is None
