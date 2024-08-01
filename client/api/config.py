"""
Module: Settings

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ Endpoint Settings

    Args:
        BaseSettings (_type_): _description_
    """
    # Similar Securities settings
    similar_securities_api_endpoint: str = Field(
        "https://query2.finance.yahoo.com/v6/finance/recommendationsbysymbol/",
        env="SIMILAR_SECURITIES_API_ENDPOINT")
    similar_securities_output: str = Field(
        "list",
        env="SIMILAR_SECURITIES_OUTPUT"
    )

    # Quote settings
    quote_api_endpoint: str = Field(
        "https://query2.finance.yahoo.com/v7/finance/quote",
        env="QUOTE_API_ENDPOINT")
    quote_cors_domain: str = Field(
        "finance.yahoo.com",
        env="QUOTE_CORS_DOMAIN")
    quote_region: str = Field(
        "US",
        env="QUOTE_REGION")
    quote_language: str = Field(
        "en-US",
        env="QUOTE_LANGUAGE")
    quote_formatted: str = Field(
        "true",
        env="QUOTE_FORMATTED")
    quote_output: str = Field(
        "dict",
        env="QUOTE_OUTPUT")

    # Crumb settings
    crumb_cookie_endpoint: str = Field(
        "https://fc.yahoo.com",
        env="CRUMB_COOKIE_ENDPOINT")
    crumb_api_endpoint: str = Field(
        "https://query1.finance.yahoo.com/v1/test/getcrumb",
        env="CRUMB_API_ENDPOINT")

    # Historic Data settings
    historic_data_api_endpoint: str = Field(
        "https://query1.finance.yahoo.com/v8/finance/chart/",
        env="HISTORIC_DATA_API_ENDPOINT"
    )
    historic_data_interval: str = Field(
        "1d",
        env="HISTORIC_DATA_INTERVAL")
    historic_data_output: str = Field(
        "dict",
        env="HISTORIC_DATA_OUTPUT")


settings = Settings()
