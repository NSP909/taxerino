export class TaxCache {
  static get(key) {
    try {
      const item = localStorage.getItem(`tax_cache_${key}`);
      if (!item) return null;

      const { value, timestamp } = JSON.parse(item);

      // Cache expires after 1 hour
      if (Date.now() - timestamp > 3600000) {
        localStorage.removeItem(`tax_cache_${key}`);
        return null;
      }

      return value;
    } catch (error) {
      console.error("Error reading from cache:", error);
      return null;
    }
  }

  static set(key, value) {
    try {
      const item = {
        value,
        timestamp: Date.now(),
      };
      localStorage.setItem(`tax_cache_${key}`, JSON.stringify(item));
    } catch (error) {
      console.error("Error writing to cache:", error);
    }
  }

  static clearTaxData() {
    try {
      localStorage.removeItem("tax_cache_tax_data");
      localStorage.removeItem("tax_cache_tax_summary");
    } catch (error) {
      console.error("Error clearing cache:", error);
    }
  }
}
