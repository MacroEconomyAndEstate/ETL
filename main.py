from domain.apartment.apartment_sales_price import ApartmentDataCollector

if __name__ == "__main__":
    collector = ApartmentDataCollector()
    collector.collect_data_for_all_regions(2006, 2023, 1, 12)
