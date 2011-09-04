package hr.fer.zemris.ga;

/**
 * Razred koji predstavlja dekoder binarnog kromosoma. Temeljem informacija
 * o minimalnim i maksimalnim vrijednostima varijabli te broju varijabli konvertira
 * niz bitova kromosoma u vrijednosti varijabli. 
 * 
 * @author marcupic
 */
public class KromosomDekoder {
	// Donje granice varijabli
	double[] xMin;
	// Gornje granice varijabli
	double[] xMax;
	// Broj bitova koji se troši na svaku varijablu
	int[] bitova;
	// Koji je najveći binarni broj pridijeljen svakoj varijabli
	int[] najveciBinarniBroj;
	// Koliko ukupno bitova ima kromosom
	int ukupnoBitova;
	// Koliko varijabli predstavlja kromosom
	int brojVarijabli;
	
	/**
	 * Konstruktor dekodera kromosoma.
	 * 
	 * @param brojVarijabli broj varijabli
	 * @param brojBitovaPoVarijabli broj bitova koji će biti korišten za svaku varijablu
	 * @param xMin donja granica (pretpostavka je da sve varijable imaju istu granicu)
	 * @param xMax gornja granica (pretpostavka je da sve varijable imaju istu granicu)
	 */
	public KromosomDekoder(int brojVarijabli, int brojBitovaPoVarijabli, double xMin, double xMax) {
		this.brojVarijabli = brojVarijabli;
		this.xMin = new double[brojVarijabli];
		this.xMax = new double[brojVarijabli];
		this.bitova = new int[brojVarijabli];
		this.najveciBinarniBroj = new int[brojVarijabli];
		for(int i = 0; i < brojVarijabli; i++) {
			this.xMin[i] = xMin;
			this.xMax[i] = xMax;
			this.bitova[i] = brojBitovaPoVarijabli;
			this.najveciBinarniBroj[i] = (1 << brojBitovaPoVarijabli) - 1;
		}
		this.ukupnoBitova = brojBitovaPoVarijabli * brojVarijabli;
	}
	
	/**
	 * Funkcija obavlja dekodiranje predanog kromosoma. Temeljem bitova u kromosomu
	 * obavlja izračun stvarnih vrijednosti koje ti bitovi predstavljaju, i u kromosomu
	 * popunjava polje {@linkplain Kromosom#varijable}.<br>
	 * Napomena: ova funkcija ne poziva automatski i izračun dobrote kromosoma u zadanoj točki;
	 * to treba obaviti naknadno.
	 * 
	 * @param k kromosom koji treba dekodirati
	 */
	public void dekodirajKromosom(Kromosom k) {
		int indeksBita = 0;
		for(int brojVarijable = 0; brojVarijable < brojVarijabli; brojVarijable++) {
			int prviBit = indeksBita;
			int zadnjiBit = prviBit + bitova[brojVarijable] - 1;
			indeksBita += bitova[brojVarijable];
			int binarniBroj = 0;
			for(int i = prviBit; i <= zadnjiBit; i++) {
				binarniBroj = binarniBroj * 2;
				if(k.bitovi[i]==1) {
					binarniBroj = binarniBroj + 1;
				}
			}
			double vrijednostVarijable = (double)binarniBroj / (double)najveciBinarniBroj[brojVarijable] * (xMax[brojVarijable]-xMin[brojVarijable]) + xMin[brojVarijable];
			k.varijable[brojVarijable] = vrijednostVarijable;
		}
	}
}
